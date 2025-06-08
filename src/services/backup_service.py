"""
Backup Service - Handles data backup and recovery operations
"""

import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import config
import logging
import json

class BackupService:
    """Service class for backup operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.backup_dir = config.EXPORTS_DIR
        self.source_file = config.EXCEL_FILE_PATH
        self.max_backups = config.MAX_BACKUPS
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_manual_backup(self, description: str = "Manual backup") -> bool:
        """Create a manual backup with timestamp"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"manual_backup_{timestamp}.xlsx"
            backup_path = self.backup_dir / backup_filename
            
            if not self.source_file.exists():
                self.logger.error("Source Excel file not found for backup")
                return False
            
            # Copy the Excel file
            shutil.copy2(self.source_file, backup_path)
            
            # Create metadata file
            metadata = {
                "backup_type": "manual",
                "created_date": datetime.now().isoformat(),
                "description": description,
                "source_file": str(self.source_file),
                "file_size": backup_path.stat().st_size,
                "app_version": config.APP_VERSION
            }
            
            metadata_path = self.backup_dir / f"manual_backup_{timestamp}.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Manual backup created: {backup_filename}")
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating manual backup: {str(e)}")
            return False
    
    def create_automatic_backup(self) -> bool:
        """Create an automatic backup (scheduled)"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"auto_backup_{timestamp}.xlsx"
            backup_path = self.backup_dir / backup_filename
            
            if not self.source_file.exists():
                self.logger.warning("Source Excel file not found for automatic backup")
                return False
            
            # Copy the Excel file
            shutil.copy2(self.source_file, backup_path)
            
            # Create metadata file
            metadata = {
                "backup_type": "automatic",
                "created_date": datetime.now().isoformat(),
                "description": "Scheduled automatic backup",
                "source_file": str(self.source_file),
                "file_size": backup_path.stat().st_size,
                "app_version": config.APP_VERSION
            }
            
            metadata_path = self.backup_dir / f"auto_backup_{timestamp}.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Automatic backup created: {backup_filename}")
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating automatic backup: {str(e)}")
            return False
    
    def create_full_system_backup(self) -> bool:
        """Create a complete system backup including all data and configuration"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"full_system_backup_{timestamp}.zip"
            backup_path = self.backup_dir / backup_filename
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
                # Add Excel file
                if self.source_file.exists():
                    backup_zip.write(self.source_file, f"data/{self.source_file.name}")
                
                # Add configuration files
                config_file = config.BASE_DIR / "config.py"
                if config_file.exists():
                    backup_zip.write(config_file, "config/config.py")
                
                # Add any additional data files
                data_dir = config.DATA_DIR
                if data_dir.exists():
                    for file_path in data_dir.rglob("*"):
                        if file_path.is_file() and file_path.suffix in ['.xlsx', '.csv', '.json']:
                            relative_path = file_path.relative_to(config.BASE_DIR)
                            backup_zip.write(file_path, str(relative_path))
                
                # Add logs (recent ones only)
                logs_dir = config.LOGS_DIR
                if logs_dir.exists():
                    for log_file in logs_dir.glob("*.log"):
                        # Only include recent log files (last 7 days)
                        if log_file.stat().st_mtime > (datetime.now() - timedelta(days=7)).timestamp():
                            backup_zip.write(log_file, f"logs/{log_file.name}")
                
                # Create system info file
                system_info = {
                    "backup_date": datetime.now().isoformat(),
                    "backup_type": "full_system",
                    "app_version": config.APP_VERSION,
                    "python_version": "3.8+",
                    "backup_contents": [
                        "Excel data files",
                        "Configuration files", 
                        "Recent log files",
                        "System metadata"
                    ]
                }
                
                # Add system info to zip
                system_info_json = json.dumps(system_info, indent=2)
                backup_zip.writestr("system_info.json", system_info_json)
            
            self.logger.info(f"Full system backup created: {backup_filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating full system backup: {str(e)}")
            return False
    
    def restore_backup(self, backup_filename: str) -> bool:
        """Restore from a backup file"""
        try:
            backup_path = self.backup_dir / backup_filename
            
            if not backup_path.exists():
                self.logger.error(f"Backup file not found: {backup_filename}")
                return False
            
            # Create a backup of current file before restore
            current_backup = f"pre_restore_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            if self.source_file.exists():
                shutil.copy2(self.source_file, self.backup_dir / current_backup)
            
            # Restore the backup
            if backup_filename.endswith('.zip'):
                # Handle full system backup
                return self._restore_full_system_backup(backup_path)
            else:
                # Handle Excel file backup
                shutil.copy2(backup_path, self.source_file)
                self.logger.info(f"Backup restored successfully: {backup_filename}")
                return True
            
        except Exception as e:
            self.logger.error(f"Error restoring backup: {str(e)}")
            return False
    
    def _restore_full_system_backup(self, backup_path: Path) -> bool:
        """Restore from a full system backup zip file"""
        try:
            with zipfile.ZipFile(backup_path, 'r') as backup_zip:
                # Extract to temporary directory first
                temp_dir = self.backup_dir / "temp_restore"
                temp_dir.mkdir(exist_ok=True)
                
                backup_zip.extractall(temp_dir)
                
                # Restore Excel file
                excel_file = temp_dir / "data" / self.source_file.name
                if excel_file.exists():
                    shutil.copy2(excel_file, self.source_file)
                
                # Clean up temp directory
                shutil.rmtree(temp_dir)
            
            self.logger.info(f"Full system backup restored: {backup_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restoring full system backup: {str(e)}")
            return False
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backup files"""
        try:
            backups = []
            
            # Find all backup files
            backup_files = list(self.backup_dir.glob("*backup*.xlsx")) + list(self.backup_dir.glob("*backup*.zip"))
            
            for backup_file in backup_files:
                try:
                    stat = backup_file.stat()
                    
                    # Try to load metadata
                    metadata_file = backup_file.with_suffix('.json')
                    metadata = {}
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                    
                    backup_info = {
                        'filename': backup_file.name,
                        'size_mb': stat.st_size / (1024 * 1024),
                        'created': datetime.fromtimestamp(stat.st_mtime),
                        'type': self._determine_backup_type(backup_file.name),
                        'description': metadata.get('description', 'No description'),
                        'app_version': metadata.get('app_version', 'Unknown')
                    }
                    
                    backups.append(backup_info)
                    
                except Exception as e:
                    self.logger.warning(f"Error reading backup file {backup_file.name}: {str(e)}")
                    continue
            
            # Sort by creation date (newest first)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
            return backups
            
        except Exception as e:
            self.logger.error(f"Error listing backups: {str(e)}")
            return []
    
    def delete_backup(self, backup_filename: str) -> bool:
        """Delete a specific backup file"""
        try:
            backup_path = self.backup_dir / backup_filename
            metadata_path = backup_path.with_suffix('.json')
            
            if backup_path.exists():
                backup_path.unlink()
                self.logger.info(f"Deleted backup file: {backup_filename}")
            
            if metadata_path.exists():
                metadata_path.unlink()
                self.logger.info(f"Deleted metadata file: {metadata_path.name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting backup: {str(e)}")
            return False
    
    def _cleanup_old_backups(self):
        """Clean up old backup files to maintain maximum count"""
        try:
            backups = self.list_backups()
            
            if len(backups) > self.max_backups:
                # Keep only the most recent backups
                backups_to_delete = backups[self.max_backups:]
                
                for backup in backups_to_delete:
                    self.delete_backup(backup['filename'])
                
                self.logger.info(f"Cleaned up {len(backups_to_delete)} old backup files")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up old backups: {str(e)}")
    
    def _determine_backup_type(self, filename: str) -> str:
        """Determine backup type from filename"""
        if 'manual' in filename:
            return 'Manual'
        elif 'auto' in filename:
            return 'Automatic'
        elif 'system' in filename:
            return 'Full System'
        else:
            return 'Unknown'
    
    def get_backup_statistics(self) -> Dict[str, Any]:
        """Get backup statistics and information"""
        try:
            backups = self.list_backups()
            
            if not backups:
                return {
                    'total_backups': 0,
                    'total_size_mb': 0,
                    'oldest_backup': None,
                    'newest_backup': None,
                    'backup_types': {}
                }
            
            total_size = sum(backup['size_mb'] for backup in backups)
            backup_types = {}
            
            for backup in backups:
                backup_type = backup['type']
                if backup_type not in backup_types:
                    backup_types[backup_type] = 0
                backup_types[backup_type] += 1
            
            return {
                'total_backups': len(backups),
                'total_size_mb': round(total_size, 2),
                'oldest_backup': backups[-1]['created'] if backups else None,
                'newest_backup': backups[0]['created'] if backups else None,
                'backup_types': backup_types,
                'average_size_mb': round(total_size / len(backups), 2) if backups else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting backup statistics: {str(e)}")
            return {}
    
    def verify_backup_integrity(self, backup_filename: str) -> Dict[str, Any]:
        """Verify the integrity of a backup file"""
        try:
            backup_path = self.backup_dir / backup_filename
            
            if not backup_path.exists():
                return {'valid': False, 'error': 'Backup file not found'}
            
            result = {'valid': True, 'checks': []}
            
            # File size check
            file_size = backup_path.stat().st_size
            if file_size == 0:
                result['valid'] = False
                result['checks'].append('File is empty')
            else:
                result['checks'].append(f'File size: {file_size / (1024 * 1024):.2f} MB')
            
            # File format check
            if backup_filename.endswith('.xlsx'):
                # Try to open as Excel file
                try:
                    import openpyxl
                    workbook = openpyxl.load_workbook(backup_path)
                    result['checks'].append(f'Excel file valid - {len(workbook.sheetnames)} sheets')
                    workbook.close()
                except Exception as e:
                    result['valid'] = False
                    result['checks'].append(f'Excel file corrupted: {str(e)}')
            
            elif backup_filename.endswith('.zip'):
                # Try to open as ZIP file
                try:
                    with zipfile.ZipFile(backup_path, 'r') as zip_file:
                        file_list = zip_file.namelist()
                        result['checks'].append(f'ZIP file valid - {len(file_list)} files')
                except Exception as e:
                    result['valid'] = False
                    result['checks'].append(f'ZIP file corrupted: {str(e)}')
            
            # Metadata check
            metadata_path = backup_path.with_suffix('.json')
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    result['checks'].append('Metadata file valid')
                    result['metadata'] = metadata
                except Exception as e:
                    result['checks'].append(f'Metadata file error: {str(e)}')
            else:
                result['checks'].append('No metadata file found')
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error verifying backup integrity: {str(e)}")
            return {'valid': False, 'error': str(e)}
    
    def schedule_automatic_backups(self) -> bool:
        """Set up automatic backup scheduling (placeholder for actual scheduler)"""
        try:
            # This is a placeholder - in a real implementation, you'd use
            # a task scheduler like APScheduler or system cron jobs
            
            self.logger.info("Automatic backup scheduling enabled")
            return True
            
        except Exception as e:
            self.logger.error(f"Error scheduling automatic backups: {str(e)}")
            return False
    
    def export_backup_log(self) -> str:
        """Export backup history as CSV"""
        try:
            backups = self.list_backups()
            
            if not backups:
                return "No backups found"
            
            # Convert to CSV format
            csv_lines = ["Filename,Type,Size(MB),Created,Description"]
            
            for backup in backups:
                csv_lines.append(
                    f"{backup['filename']},{backup['type']},{backup['size_mb']:.2f},"
                    f"{backup['created'].strftime('%Y-%m-%d %H:%M:%S')},{backup['description']}"
                )
            
            return "\n".join(csv_lines)
            
        except Exception as e:
            self.logger.error(f"Error exporting backup log: {str(e)}")
            return f"Error: {str(e)}"