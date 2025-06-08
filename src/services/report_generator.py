"""
Report Generator Service - Creates various business reports and analytics
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Tuple
import config
from src.services.excel_service import ExcelService
from src.services.stock_calculator import StockCalculator
import io
import base64
import logging

class ReportGenerator:
    """Service class for generating business reports"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.excel_service = ExcelService()
        self.stock_calculator = StockCalculator()
    
    def generate_stock_summary_report(self, as_of_date: date = None) -> Dict[str, Any]:
        """Generate comprehensive stock summary report"""
        try:
            if as_of_date is None:
                as_of_date = date.today()
            
            # Get stock data
            stock_data = self.excel_service.read_stock_data()
            
            if stock_data is None or stock_data.empty:
                return self._get_empty_report("Stock Summary")
            
            # Calculate stock summary
            summary = self.stock_calculator.calculate_stock_summary(stock_data)
            
            # Generate detailed analysis
            report = {
                'report_type': 'Stock Summary',
                'generated_date': datetime.now(),
                'as_of_date': as_of_date,
                'summary': summary,
                'detailed_data': stock_data.to_dict('records'),
                'charts': self._generate_stock_charts(stock_data),
                'recommendations': self._generate_stock_recommendations(stock_data, summary)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating stock summary report: {str(e)}")
            return self._get_empty_report("Stock Summary", error=str(e))
    
    def generate_sales_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate sales analysis report"""
        try:
            # For now, generate sample sales data (replace with actual data)
            sales_data = self._generate_sample_sales_data(start_date, end_date)
            
            # Calculate sales metrics
            sales_summary = self._calculate_sales_metrics(sales_data, start_date, end_date)
            
            # Generate sales charts
            sales_charts = self._generate_sales_charts(sales_data)
            
            report = {
                'report_type': 'Sales Analysis',
                'generated_date': datetime.now(),
                'period_start': start_date,
                'period_end': end_date,
                'summary': sales_summary,
                'detailed_data': sales_data.to_dict('records'),
                'charts': sales_charts,
                'trends': self._analyze_sales_trends(sales_data)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating sales report: {str(e)}")
            return self._get_empty_report("Sales Analysis", error=str(e))
    
    def generate_financial_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate financial performance report"""
        try:
            # Generate sample financial data (replace with actual calculations)
            financial_data = self._generate_sample_financial_data(start_date, end_date)
            
            # Calculate financial metrics
            financial_summary = self._calculate_financial_metrics(financial_data)
            
            report = {
                'report_type': 'Financial Performance',
                'generated_date': datetime.now(),
                'period_start': start_date,
                'period_end': end_date,
                'summary': financial_summary,
                'profit_loss': self._calculate_profit_loss(financial_data),
                'cash_flow': self._calculate_cash_flow(financial_data),
                'charts': self._generate_financial_charts(financial_data)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating financial report: {str(e)}")
            return self._get_empty_report("Financial Performance", error=str(e))
    
    def generate_production_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate production analysis report"""
        try:
            # Generate sample production data (replace with actual data)
            production_data = self._generate_sample_production_data(start_date, end_date)
            
            # Calculate production metrics
            production_summary = self._calculate_production_metrics(production_data)
            
            report = {
                'report_type': 'Production Analysis',
                'generated_date': datetime.now(),
                'period_start': start_date,
                'period_end': end_date,
                'summary': production_summary,
                'detailed_data': production_data.to_dict('records'),
                'efficiency_analysis': self._analyze_production_efficiency(production_data),
                'charts': self._generate_production_charts(production_data)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating production report: {str(e)}")
            return self._get_empty_report("Production Analysis", error=str(e))
    
    def generate_custom_report(self, report_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate custom report based on configuration"""
        try:
            report_type = report_config.get('type', 'Custom Analysis')
            date_range = report_config.get('date_range', {})
            filters = report_config.get('filters', {})
            
            # Start with base report structure
            report = {
                'report_type': report_type,
                'generated_date': datetime.now(),
                'config': report_config,
                'data': {},
                'charts': {},
                'summary': {}
            }
            
            # Generate report based on type
            if report_type == 'Stock Analysis':
                stock_data = self.excel_service.read_stock_data()
                if stock_data is not None:
                    report['data'] = self._filter_data(stock_data, filters).to_dict('records')
                    report['summary'] = self.stock_calculator.calculate_stock_summary(stock_data)
            
            elif report_type == 'Sales Summary':
                start_date = date_range.get('start', date.today() - timedelta(days=30))
                end_date = date_range.get('end', date.today())
                sales_data = self._generate_sample_sales_data(start_date, end_date)
                report['data'] = self._filter_data(sales_data, filters).to_dict('records')
                report['summary'] = self._calculate_sales_metrics(sales_data, start_date, end_date)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating custom report: {str(e)}")
            return self._get_empty_report("Custom Analysis", error=str(e))
    
    def export_report_to_excel(self, report_data: Dict[str, Any]) -> bytes:
        """Export report data to Excel format"""
        try:
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Summary sheet
                if 'summary' in report_data:
                    summary_df = pd.DataFrame([report_data['summary']])
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Detailed data sheet
                if 'detailed_data' in report_data:
                    data_df = pd.DataFrame(report_data['detailed_data'])
                    data_df.to_excel(writer, sheet_name='Detailed Data', index=False)
                
                # Additional sheets based on report type
                if report_data.get('report_type') == 'Financial Performance':
                    if 'profit_loss' in report_data:
                        pl_df = pd.DataFrame([report_data['profit_loss']])
                        pl_df.to_excel(writer, sheet_name='Profit & Loss', index=False)
                
                # Metadata sheet
                metadata = {
                    'Report Type': [report_data.get('report_type', 'Unknown')],
                    'Generated Date': [report_data.get('generated_date', datetime.now())],
                    'Generated By': ['Inventory Management System'],
                    'Version': [config.APP_VERSION]
                }
                metadata_df = pd.DataFrame(metadata)
                metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
            
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            self.logger.error(f"Error exporting report to Excel: {str(e)}")
            return b''
    
    def export_report_to_csv(self, report_data: Dict[str, Any]) -> str:
        """Export report data to CSV format"""
        try:
            if 'detailed_data' in report_data:
                data_df = pd.DataFrame(report_data['detailed_data'])
                return data_df.to_csv(index=False)
            elif 'summary' in report_data:
                summary_df = pd.DataFrame([report_data['summary']])
                return summary_df.to_csv(index=False)
            else:
                return "No data available for export"
                
        except Exception as e:
            self.logger.error(f"Error exporting report to CSV: {str(e)}")
            return f"Error exporting data: {str(e)}"
    
    # Private helper methods
    
    def _get_empty_report(self, report_type: str, error: str = None) -> Dict[str, Any]:
        """Return empty report structure"""
        return {
            'report_type': report_type,
            'generated_date': datetime.now(),
            'summary': {},
            'detailed_data': [],
            'charts': {},
            'error': error
        }
    
    def _generate_stock_charts(self, stock_data: pd.DataFrame) -> Dict[str, str]:
        """Generate charts for stock data"""
        charts = {}
        
        try:
            # Stock levels chart
            if not stock_data.empty:
                fig = px.bar(
                    stock_data,
                    x='product_name' if 'product_name' in stock_data.columns else stock_data.index,
                    y='current_stock' if 'current_stock' in stock_data.columns else stock_data.iloc[:, 0],
                    title='Current Stock Levels'
                )
                charts['stock_levels'] = self._fig_to_base64(fig)
                
                # Stock value distribution
                if 'stock_value' in stock_data.columns:
                    fig = px.pie(
                        stock_data,
                        values='stock_value',
                        names='product_name' if 'product_name' in stock_data.columns else stock_data.index,
                        title='Stock Value Distribution'
                    )
                    charts['value_distribution'] = self._fig_to_base64(fig)
                    
        except Exception as e:
            self.logger.error(f"Error generating stock charts: {str(e)}")
        
        return charts
    
    def _generate_sales_charts(self, sales_data: pd.DataFrame) -> Dict[str, str]:
        """Generate charts for sales data"""
        charts = {}
        
        try:
            if not sales_data.empty:
                # Daily sales trend
                if 'date' in sales_data.columns and 'revenue' in sales_data.columns:
                    daily_sales = sales_data.groupby('date')['revenue'].sum().reset_index()
                    fig = px.line(daily_sales, x='date', y='revenue', title='Daily Sales Trend')
                    charts['daily_trend'] = self._fig_to_base64(fig)
                
                # Sales by product
                if 'product' in sales_data.columns and 'quantity' in sales_data.columns:
                    product_sales = sales_data.groupby('product')['quantity'].sum().reset_index()
                    fig = px.bar(product_sales, x='product', y='quantity', title='Sales by Product')
                    charts['product_sales'] = self._fig_to_base64(fig)
                    
        except Exception as e:
            self.logger.error(f"Error generating sales charts: {str(e)}")
        
        return charts
    
    def _generate_financial_charts(self, financial_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate charts for financial data"""
        charts = {}
        
        try:
            # Revenue vs Expenses
            categories = ['Revenue', 'Expenses', 'Profit']
            values = [
                financial_data.get('total_revenue', 0),
                financial_data.get('total_expenses', 0),
                financial_data.get('net_profit', 0)
            ]
            
            fig = px.bar(x=categories, y=values, title='Financial Overview')
            charts['financial_overview'] = self._fig_to_base64(fig)
            
        except Exception as e:
            self.logger.error(f"Error generating financial charts: {str(e)}")
        
        return charts
    
    def _generate_production_charts(self, production_data: pd.DataFrame) -> Dict[str, str]:
        """Generate charts for production data"""
        charts = {}
        
        try:
            if not production_data.empty:
                # Production trend
                if 'date' in production_data.columns and 'total_output' in production_data.columns:
                    fig = px.line(production_data, x='date', y='total_output', title='Production Output Trend')
                    charts['production_trend'] = self._fig_to_base64(fig)
                
                # Efficiency trend
                if 'date' in production_data.columns and 'efficiency' in production_data.columns:
                    fig = px.line(production_data, x='date', y='efficiency', title='Production Efficiency Trend')
                    charts['efficiency_trend'] = self._fig_to_base64(fig)
                    
        except Exception as e:
            self.logger.error(f"Error generating production charts: {str(e)}")
        
        return charts
    
    def _fig_to_base64(self, fig) -> str:
        """Convert plotly figure to base64 string"""
        try:
            img_bytes = fig.to_image(format="png")
            img_base64 = base64.b64encode(img_bytes).decode()
            return f"data:image/png;base64,{img_base64}"
        except Exception as e:
            self.logger.error(f"Error converting figure to base64: {str(e)}")
            return ""
    
    def _generate_sample_sales_data(self, start_date: date, end_date: date) -> pd.DataFrame:
        """Generate sample sales data for testing"""
        import numpy as np
        
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        data = []
        
        for date in dates:
            for weight in config.PRODUCT_WEIGHTS:
                if np.random.random() > 0.3:  # Random sales occurrence
                    quantity = np.random.randint(1, 20)
                    unit_price = weight * 50 + np.random.randint(-10, 20)
                    data.append({
                        'date': date,
                        'product': f'{weight}kg',
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'revenue': quantity * unit_price,
                        'channel': np.random.choice(config.SALES_CHANNELS)
                    })
        
        return pd.DataFrame(data)
    
    def _generate_sample_financial_data(self, start_date: date, end_date: date) -> Dict[str, float]:
        """Generate sample financial data"""
        import numpy as np
        
        days = (end_date - start_date).days + 1
        
        return {
            'total_revenue': np.random.randint(50000, 150000),
            'total_expenses': np.random.randint(30000, 80000),
            'net_profit': 0,  # Will be calculated
            'gross_margin': np.random.uniform(20, 40),
            'operating_expenses': np.random.randint(10000, 30000)
        }
    
    def _generate_sample_production_data(self, start_date: date, end_date: date) -> pd.DataFrame:
        """Generate sample production data"""
        import numpy as np
        
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        data = []
        
        for date in dates:
            if np.random.random() > 0.2:  # Production on 80% of days
                data.append({
                    'date': date,
                    'batch_number': f'BATCH-{date.strftime("%m%d")}-{np.random.randint(1, 4)}',
                    'raw_material_kg': np.random.randint(80, 150),
                    'total_output': np.random.randint(200, 500),
                    'efficiency': np.random.uniform(85, 98),
                    'operator': f'Operator {np.random.randint(1, 4)}'
                })
        
        return pd.DataFrame(data)
    
    def _calculate_sales_metrics(self, sales_data: pd.DataFrame, start_date: date, end_date: date) -> Dict[str, Any]:
        """Calculate sales metrics"""
        if sales_data.empty:
            return {}
        
        return {
            'total_revenue': sales_data['revenue'].sum() if 'revenue' in sales_data.columns else 0,
            'total_units_sold': sales_data['quantity'].sum() if 'quantity' in sales_data.columns else 0,
            'average_order_value': sales_data['revenue'].mean() if 'revenue' in sales_data.columns else 0,
            'total_transactions': len(sales_data),
            'period_days': (end_date - start_date).days + 1
        }
    
    def _calculate_financial_metrics(self, financial_data: Dict[str, float]) -> Dict[str, float]:
        """Calculate financial metrics"""
        revenue = financial_data.get('total_revenue', 0)
        expenses = financial_data.get('total_expenses', 0)
        
        financial_data['net_profit'] = revenue - expenses
        financial_data['profit_margin'] = (financial_data['net_profit'] / revenue * 100) if revenue > 0 else 0
        
        return financial_data
    
    def _calculate_production_metrics(self, production_data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate production metrics"""
        if production_data.empty:
            return {}
        
        return {
            'total_batches': len(production_data),
            'total_output': production_data['total_output'].sum() if 'total_output' in production_data.columns else 0,
            'average_efficiency': production_data['efficiency'].mean() if 'efficiency' in production_data.columns else 0,
            'total_raw_material': production_data['raw_material_kg'].sum() if 'raw_material_kg' in production_data.columns else 0
        }
    
    def _generate_stock_recommendations(self, stock_data: pd.DataFrame, summary: Dict[str, Any]) -> List[str]:
        """Generate stock recommendations"""
        recommendations = []
        
        if summary.get('low_stock_items', 0) > 0:
            recommendations.append(f"⚠️ {summary['low_stock_items']} items are below minimum stock level - immediate reorder recommended")
        
        if summary.get('critical_stock_items', 0) > 0:
            recommendations.append(f"🚨 {summary['critical_stock_items']} items are critically low - urgent action required")
        
        if summary.get('overstocked_items', 0) > 0:
            recommendations.append(f"📈 {summary['overstocked_items']} items are overstocked - consider promotional activities")
        
        return recommendations
    
    def _analyze_sales_trends(self, sales_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze sales trends"""
        if sales_data.empty:
            return {}
        
        # Simple trend analysis
        if 'date' in sales_data.columns and 'revenue' in sales_data.columns:
            daily_revenue = sales_data.groupby('date')['revenue'].sum()
            
            if len(daily_revenue) > 1:
                trend = "increasing" if daily_revenue.iloc[-1] > daily_revenue.iloc[0] else "decreasing"
                return {'overall_trend': trend}
        
        return {}
    
    def _analyze_production_efficiency(self, production_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze production efficiency"""
        if production_data.empty or 'efficiency' not in production_data.columns:
            return {}
        
        return {
            'average_efficiency': production_data['efficiency'].mean(),
            'efficiency_trend': 'stable',  # Simplified
            'best_efficiency': production_data['efficiency'].max(),
            'worst_efficiency': production_data['efficiency'].min()
        }
    
    def _calculate_profit_loss(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate profit and loss statement"""
        return {
            'revenue': financial_data.get('total_revenue', 0),
            'cost_of_goods': financial_data.get('total_expenses', 0) * 0.6,  # Estimate
            'gross_profit': financial_data.get('total_revenue', 0) - (financial_data.get('total_expenses', 0) * 0.6),
            'operating_expenses': financial_data.get('operating_expenses', 0),
            'net_profit': financial_data.get('net_profit', 0)
        }
    
    def _calculate_cash_flow(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate cash flow statement"""
        return {
            'cash_from_operations': financial_data.get('net_profit', 0),
            'cash_from_investing': 0,  # Simplified
            'cash_from_financing': 0,  # Simplified
            'net_cash_flow': financial_data.get('net_profit', 0)
        }
    
    def _filter_data(self, data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to data"""
        filtered_data = data.copy()
        
        # Apply filters based on the filters dictionary
        for column, filter_value in filters.items():
            if column in filtered_data.columns:
                if isinstance(filter_value, list):
                    filtered_data = filtered_data[filtered_data[column].isin(filter_value)]
                else:
                    filtered_data = filtered_data[filtered_data[column] == filter_value]
        
        return filtered_data