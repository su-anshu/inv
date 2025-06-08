"""
Report Data Model - Defines report structures and operations
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, date
from enum import Enum

class ReportType(Enum):
    """Report type enumeration"""
    STOCK_SUMMARY = "stock_summary"
    SALES_ANALYSIS = "sales_analysis"
    PURCHASE_REPORT = "purchase_report"
    PRODUCTION_REPORT = "production_report"
    FINANCIAL_SUMMARY = "financial_summary"
    INVENTORY_VALUATION = "inventory_valuation"
    ABC_ANALYSIS = "abc_analysis"
    CUSTOM_REPORT = "custom_report"

class ReportFormat(Enum):
    """Report format enumeration"""
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    HTML = "html"

class ReportStatus(Enum):
    """Report generation status"""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"

@dataclass
class ReportMetadata:
    """Report metadata structure"""
    
    report_id: str
    report_name: str
    report_type: ReportType
    description: str = ""
    generated_by: str = "System"
    generated_date: datetime = field(default_factory=datetime.now)
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    filters: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: ReportStatus = ReportStatus.PENDING
    format: ReportFormat = ReportFormat.EXCEL
    file_size_mb: float = 0.0
    expiry_date: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'report_id': self.report_id,
            'report_name': self.report_name,
            'report_type': self.report_type.value,
            'description': self.description,
            'generated_by': self.generated_by,
            'generated_date': self.generated_date.isoformat(),
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'filters': self.filters,
            'parameters': self.parameters,
            'status': self.status.value,
            'format': self.format.value,
            'file_size_mb': self.file_size_mb,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None
        }

@dataclass
class StockSummaryReport:
    """Stock summary report structure"""
    
    metadata: ReportMetadata
    summary: Dict[str, Any] = field(default_factory=dict)
    stock_items: List[Dict[str, Any]] = field(default_factory=list)
    low_stock_alerts: List[Dict[str, Any]] = field(default_factory=list)
    reorder_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    stock_value_breakdown: Dict[str, float] = field(default_factory=dict)
    charts: Dict[str, str] = field(default_factory=dict)
    
    def calculate_summary(self, inventory_data: List[Dict[str, Any]]) -> None:
        """Calculate summary statistics"""
        if not inventory_data:
            return
        
        total_items = len(inventory_data)
        total_stock = sum(item.get('current_stock', 0) for item in inventory_data)
        total_value = sum(item.get('stock_value', 0) for item in inventory_data)
        
        low_stock_count = len([item for item in inventory_data 
                              if item.get('stock_status') in ['low', 'critical', 'out_of_stock']])
        
        self.summary = {
            'total_products': total_items,
            'total_stock_units': total_stock,
            'total_stock_value': total_value,
            'average_stock_per_product': total_stock / total_items if total_items > 0 else 0,
            'low_stock_items': low_stock_count,
            'stock_coverage_days': 30,  # Placeholder calculation
            'last_updated': datetime.now().isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'metadata': self.metadata.to_dict(),
            'summary': self.summary,
            'stock_items': self.stock_items,
            'low_stock_alerts': self.low_stock_alerts,
            'reorder_recommendations': self.reorder_recommendations,
            'stock_value_breakdown': self.stock_value_breakdown,
            'charts': self.charts
        }

@dataclass
class SalesAnalysisReport:
    """Sales analysis report structure"""
    
    metadata: ReportMetadata
    summary: Dict[str, Any] = field(default_factory=dict)
    sales_data: List[Dict[str, Any]] = field(default_factory=list)
    product_performance: List[Dict[str, Any]] = field(default_factory=list)
    channel_performance: List[Dict[str, Any]] = field(default_factory=list)
    trends: Dict[str, Any] = field(default_factory=dict)
    charts: Dict[str, str] = field(default_factory=dict)
    
    def calculate_summary(self, sales_transactions: List[Dict[str, Any]]) -> None:
        """Calculate sales summary"""
        if not sales_transactions:
            return
        
        total_revenue = sum(tx.get('total_amount', 0) for tx in sales_transactions)
        total_quantity = sum(tx.get('quantity', 0) for tx in sales_transactions)
        total_orders = len(sales_transactions)
        
        self.summary = {
            'total_revenue': total_revenue,
            'total_quantity_sold': total_quantity,
            'total_orders': total_orders,
            'average_order_value': total_revenue / total_orders if total_orders > 0 else 0,
            'average_selling_price': total_revenue / total_quantity if total_quantity > 0 else 0,
            'period_start': self.metadata.period_start.isoformat() if self.metadata.period_start else None,
            'period_end': self.metadata.period_end.isoformat() if self.metadata.period_end else None
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'metadata': self.metadata.to_dict(),
            'summary': self.summary,
            'sales_data': self.sales_data,
            'product_performance': self.product_performance,
            'channel_performance': self.channel_performance,
            'trends': self.trends,
            'charts': self.charts
        }

@dataclass
class FinancialSummaryReport:
    """Financial summary report structure"""
    
    metadata: ReportMetadata
    profit_loss: Dict[str, float] = field(default_factory=dict)
    cash_flow: Dict[str, float] = field(default_factory=dict)
    balance_sheet: Dict[str, float] = field(default_factory=dict)
    key_metrics: Dict[str, float] = field(default_factory=dict)
    variance_analysis: Dict[str, Any] = field(default_factory=dict)
    charts: Dict[str, str] = field(default_factory=dict)
    
    def calculate_profit_loss(self, sales_data: List[Dict[str, Any]], purchase_data: List[Dict[str, Any]]) -> None:
        """Calculate profit and loss statement"""
        revenue = sum(sale.get('total_amount', 0) for sale in sales_data)
        cost_of_goods = sum(purchase.get('total_amount', 0) for purchase in purchase_data)
        
        gross_profit = revenue - cost_of_goods
        operating_expenses = cost_of_goods * 0.2  # Estimate
        net_profit = gross_profit - operating_expenses
        
        self.profit_loss = {
            'revenue': revenue,
            'cost_of_goods_sold': cost_of_goods,
            'gross_profit': gross_profit,
            'gross_margin_percentage': (gross_profit / revenue * 100) if revenue > 0 else 0,
            'operating_expenses': operating_expenses,
            'net_profit': net_profit,
            'net_margin_percentage': (net_profit / revenue * 100) if revenue > 0 else 0
        }
    
    def calculate_key_metrics(self) -> None:
        """Calculate key financial metrics"""
        self.key_metrics = {
            'return_on_investment': 15.5,  # Placeholder
            'current_ratio': 2.1,  # Placeholder
            'quick_ratio': 1.8,  # Placeholder
            'debt_to_equity': 0.3,  # Placeholder
            'inventory_turnover': 4.2,  # Placeholder
            'days_sales_outstanding': 45  # Placeholder
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'metadata': self.metadata.to_dict(),
            'profit_loss': self.profit_loss,
            'cash_flow': self.cash_flow,
            'balance_sheet': self.balance_sheet,
            'key_metrics': self.key_metrics,
            'variance_analysis': self.variance_analysis,
            'charts': self.charts
        }

class ReportLibrary:
    """Manages report templates and generated reports"""
    
    def __init__(self):
        self.reports: Dict[str, Dict[str, Any]] = {}
        self.templates: Dict[ReportType, Dict[str, Any]] = {}
        self._initialize_templates()
    
    def _initialize_templates(self) -> None:
        """Initialize report templates"""
        self.templates = {
            ReportType.STOCK_SUMMARY: {
                'name': 'Stock Summary Report',
                'description': 'Comprehensive overview of current inventory levels',
                'required_data': ['inventory_data'],
                'sections': ['summary', 'stock_items', 'alerts', 'recommendations'],
                'charts': ['stock_levels', 'value_distribution', 'status_breakdown']
            },
            ReportType.SALES_ANALYSIS: {
                'name': 'Sales Analysis Report',
                'description': 'Detailed analysis of sales performance and trends',
                'required_data': ['sales_transactions'],
                'sections': ['summary', 'product_performance', 'channel_analysis', 'trends'],
                'charts': ['sales_trend', 'product_breakdown', 'channel_performance']
            },
            ReportType.FINANCIAL_SUMMARY: {
                'name': 'Financial Summary Report',
                'description': 'Financial performance and key metrics analysis',
                'required_data': ['sales_data', 'purchase_data', 'expense_data'],
                'sections': ['profit_loss', 'cash_flow', 'key_metrics', 'variance_analysis'],
                'charts': ['revenue_trend', 'profit_margin', 'expense_breakdown']
            }
        }
    
    def create_report_metadata(self, report_type: ReportType, report_name: str, **kwargs) -> ReportMetadata:
        """Create report metadata"""
        import uuid
        
        return ReportMetadata(
            report_id=str(uuid.uuid4()),
            report_name=report_name,
            report_type=report_type,
            description=kwargs.get('description', ''),
            generated_by=kwargs.get('generated_by', 'System'),
            period_start=kwargs.get('period_start'),
            period_end=kwargs.get('period_end'),
            filters=kwargs.get('filters', {}),
            parameters=kwargs.get('parameters', {}),
            format=kwargs.get('format', ReportFormat.EXCEL)
        )
    
    def generate_stock_summary_report(self, inventory_data: List[Dict[str, Any]], **kwargs) -> StockSummaryReport:
        """Generate stock summary report"""
        metadata = self.create_report_metadata(
            ReportType.STOCK_SUMMARY,
            "Stock Summary Report",
            **kwargs
        )
        
        report = StockSummaryReport(metadata=metadata)
        report.calculate_summary(inventory_data)
        report.stock_items = inventory_data
        
        # Calculate alerts and recommendations
        report.low_stock_alerts = [
            item for item in inventory_data 
            if item.get('stock_status') in ['low', 'critical', 'out_of_stock']
        ]
        
        report.reorder_recommendations = [
            {
                'product_name': item.get('product_name', ''),
                'current_stock': item.get('current_stock', 0),
                'recommended_order': item.get('reorder_quantity', 0),
                'urgency': 'High' if item.get('stock_status') == 'critical' else 'Medium'
            }
            for item in report.low_stock_alerts
        ]
        
        # Store report
        self.reports[metadata.report_id] = report.to_dict()
        
        return report
    
    def generate_sales_analysis_report(self, sales_data: List[Dict[str, Any]], **kwargs) -> SalesAnalysisReport:
        """Generate sales analysis report"""
        metadata = self.create_report_metadata(
            ReportType.SALES_ANALYSIS,
            "Sales Analysis Report",
            **kwargs
        )
        
        report = SalesAnalysisReport(metadata=metadata)
        report.calculate_summary(sales_data)
        report.sales_data = sales_data
        
        # Calculate product performance
        product_performance = {}
        for sale in sales_data:
            product = sale.get('product_name', 'Unknown')
            if product not in product_performance:
                product_performance[product] = {
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'orders': 0
                }
            
            product_performance[product]['total_quantity'] += sale.get('quantity', 0)
            product_performance[product]['total_revenue'] += sale.get('total_amount', 0)
            product_performance[product]['orders'] += 1
        
        report.product_performance = [
            {
                'product_name': product,
                'total_quantity': data['total_quantity'],
                'total_revenue': data['total_revenue'],
                'orders': data['orders'],
                'average_order_value': data['total_revenue'] / data['orders'] if data['orders'] > 0 else 0
            }
            for product, data in product_performance.items()
        ]
        
        # Store report
        self.reports[metadata.report_id] = report.to_dict()
        
        return report
    
    def generate_financial_summary_report(self, sales_data: List[Dict[str, Any]], purchase_data: List[Dict[str, Any]], **kwargs) -> FinancialSummaryReport:
        """Generate financial summary report"""
        metadata = self.create_report_metadata(
            ReportType.FINANCIAL_SUMMARY,
            "Financial Summary Report",
            **kwargs
        )
        
        report = FinancialSummaryReport(metadata=metadata)
        report.calculate_profit_loss(sales_data, purchase_data)
        report.calculate_key_metrics()
        
        # Store report
        self.reports[metadata.report_id] = report.to_dict()
        
        return report
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get generated report by ID"""
        return self.reports.get(report_id)
    
    def list_reports(self, report_type: Optional[ReportType] = None) -> List[Dict[str, Any]]:
        """List all generated reports"""
        reports = []
        
        for report_id, report_data in self.reports.items():
            metadata = report_data.get('metadata', {})
            
            if report_type is None or metadata.get('report_type') == report_type.value:
                reports.append({
                    'report_id': report_id,
                    'report_name': metadata.get('report_name', ''),
                    'report_type': metadata.get('report_type', ''),
                    'generated_date': metadata.get('generated_date', ''),
                    'status': metadata.get('status', ''),
                    'format': metadata.get('format', ''),
                    'file_size_mb': metadata.get('file_size_mb', 0)
                })
        
        # Sort by generation date (newest first)
        reports.sort(key=lambda x: x['generated_date'], reverse=True)
        
        return reports
    
    def delete_report(self, report_id: str) -> bool:
        """Delete a generated report"""
        if report_id in self.reports:
            del self.reports[report_id]
            return True
        return False
    
    def get_report_template(self, report_type: ReportType) -> Optional[Dict[str, Any]]:
        """Get report template information"""
        return self.templates.get(report_type)
    
    def export_report_data(self, report_id: str, format: ReportFormat = ReportFormat.JSON) -> Optional[Any]:
        """Export report data in specified format"""
        if report_id not in self.reports:
            return None
        
        report_data = self.reports[report_id]
        
        if format == ReportFormat.JSON:
            import json
            return json.dumps(report_data, indent=2)
        
        elif format == ReportFormat.CSV:
            import pandas as pd
            
            # Convert main data sections to CSV
            csv_data = ""
            
            if 'stock_items' in report_data:
                df = pd.DataFrame(report_data['stock_items'])
                csv_data += "Stock Items:\n"
                csv_data += df.to_csv(index=False)
                csv_data += "\n\n"
            
            if 'sales_data' in report_data:
                df = pd.DataFrame(report_data['sales_data'])
                csv_data += "Sales Data:\n"
                csv_data += df.to_csv(index=False)
            
            return csv_data
        
        elif format == ReportFormat.EXCEL:
            import pandas as pd
            import io
            
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Write summary
                if 'summary' in report_data:
                    summary_df = pd.DataFrame([report_data['summary']])
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Write detailed data
                if 'stock_items' in report_data:
                    stock_df = pd.DataFrame(report_data['stock_items'])
                    stock_df.to_excel(writer, sheet_name='Stock Items', index=False)
                
                if 'sales_data' in report_data:
                    sales_df = pd.DataFrame(report_data['sales_data'])
                    sales_df.to_excel(writer, sheet_name='Sales Data', index=False)
            
            output.seek(0)
            return output.getvalue()
        
        return None
    
    def schedule_report_generation(self, report_type: ReportType, schedule: str, **kwargs) -> str:
        """Schedule automatic report generation"""
        import uuid
        
        schedule_id = str(uuid.uuid4())
        
        # This would integrate with a scheduler like APScheduler in a real implementation
        # For now, just return the schedule ID
        
        return schedule_id
    
    def get_report_statistics(self) -> Dict[str, Any]:
        """Get statistics about generated reports"""
        total_reports = len(self.reports)
        
        type_counts = {}
        format_counts = {}
        total_size = 0
        
        for report_data in self.reports.values():
            metadata = report_data.get('metadata', {})
            
            report_type = metadata.get('report_type', 'unknown')
            type_counts[report_type] = type_counts.get(report_type, 0) + 1
            
            report_format = metadata.get('format', 'unknown')
            format_counts[report_format] = format_counts.get(report_format, 0) + 1
            
            total_size += metadata.get('file_size_mb', 0)
        
        return {
            'total_reports': total_reports,
            'reports_by_type': type_counts,
            'reports_by_format': format_counts,
            'total_size_mb': round(total_size, 2),
            'average_size_mb': round(total_size / total_reports, 2) if total_reports > 0 else 0
        }