# 📦 Inventory Management System

A comprehensive inventory management system built with Streamlit and Excel integration for small to medium businesses.

## 🚀 Features

- **Live Dashboard**: Real-time inventory overview with KPIs and charts
- **Data Entry Portal**: Easy forms for daily operations (sales, purchases, production)
- **Excel Integration**: Seamless integration with existing Excel files
- **Reports & Analytics**: Detailed reports and business insights
- **Backup System**: Automated backups and data protection
- **Multi-Channel Support**: Amazon FBA, Flipkart, and other sales channels

## 📋 Requirements

- Python 3.8 or higher
- Excel file with specific sheet structure
- Web browser (Chrome, Firefox, Safari)

## 🔧 Installation

1. **Clone or download the project**
   ```bash
   git clone <your-repo-url>
   cd inventory_management_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv inventory_env
   
   # Windows
   inventory_env\Scripts\activate
   
   # macOS/Linux
   source inventory_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your Excel file**
   - Copy your Excel file to `data/uploads/stock_report.xlsx`
   - Ensure it has the required sheets: "stock sheet", "Return", "Packaging", etc.

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

6. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

## 📂 Project Structure

```
inventory_management_system/
├── main.py                 # Main application
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── data/                  # Data storage
│   ├── uploads/          # Excel files
│   ├── exports/          # Reports
│   └── templates/        # Templates
├── src/                  # Source code
│   ├── components/       # UI components
│   ├── pages/           # Application pages
│   ├── services/        # Business logic
│   ├── models/          # Data models
│   └── utils/           # Utilities
├── static/              # Static assets
└── logs/               # Application logs
```

## 📊 Excel File Requirements

Your Excel file should contain these sheets:

1. **stock sheet** - Main inventory data
2. **Return** - Return transactions
3. **Packaging** - Packaging materials
4. **Cartoons report** - Packaging reports
5. **Packging** - Additional packaging data

## 🎯 Usage

### Dashboard
- View real-time inventory metrics
- Monitor stock levels and alerts
- Analyze sales trends and performance

### Data Entry
- Record daily sales, purchases, production
- Manage product information
- Bulk upload via CSV/Excel
- Quick entry for common operations

### Reports
- Generate detailed analytics reports
- Export data in multiple formats
- Track business performance over time

## 🔧 Configuration

Modify `config.py` to customize:

- Product weights and details
- Sales channels
- Stock thresholds
- Backup settings
- UI preferences

## 🚨 Troubleshooting

**Common Issues:**

1. **"Excel file not found"**
   - Ensure your Excel file is at `data/uploads/stock_report.xlsx`
   - Check file permissions

2. **"Module not found"**
   - Activate virtual environment
   - Install requirements: `pip install -r requirements.txt`

3. **"Permission denied"**
   - Close Excel file if it's open
   - Check file/folder permissions

4. **"Import errors"**
   - Ensure you're in the correct directory
   - Check Python path in error messages

## 📝 Support

For issues and questions:

1. Check the troubleshooting section
2. Review log files in `logs/app.log`
3. Ensure all requirements are installed
4. Verify Excel file structure matches requirements

## 📈 Future Enhancements

- API integration with Amazon/Flipkart
- Barcode scanning support
- Multi-user authentication
- Cloud backup integration
- Mobile app companion
- Advanced ML forecasting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**Version:** 1.0.0  
**Last Updated:** June 8, 2025  
**Author:** Your Name