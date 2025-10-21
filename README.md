# O2O优惠券特征分析与处理Web应用

[English](#english-version) | [中文](#中文版本)

## 中文版本

### 项目简介

这是一个基于Flask和MySQL的O2O优惠券特征分析与处理Web应用程序。该系统能够上传、处理和分析O2O优惠券数据，生成可视化统计图表，并将处理后的数据存储到MySQL数据库中。

### 演示视频

📺 [观看演示视频](https://youtu.be/EuD5We0Vg9A)

### 主要功能

1. **CSV文件上传与处理**
   - 支持上传O2O优惠券原始数据（CSV格式）
   - 自动解析和预处理数据

2. **特征工程**
   - 日期格式转换处理（将YYYYMMDD格式转换为标准日期格式）
   - 自动生成标签列（label）：
     - `1`: 15天内使用优惠券的用户
     - `-1`: 领取优惠券但未使用的用户
     - `0`: 15天后使用优惠券的用户
     - `None`: 未领取优惠券的用户

3. **数据可视化**
   - **缺失值统计图**：展示各列的缺失值数量
   - **标签分布图**：展示不同标签类型的数量分布
   - **优惠券类型占比图**：饼图展示不同折扣率的优惠券分布

4. **数据库集成**
   - 与MySQL数据库集成，支持数据持久化存储
   - 异步数据上传，提升处理效率
   - 支持数据查询和导出

5. **动态背景**
   - 集成Bing每日壁纸作为动态背景
   - 自动轮播展示

### 技术栈

- **后端框架**: Flask (Python)
- **数据处理**: Pandas, NumPy
- **数据可视化**: Matplotlib
- **数据库**: MySQL 5.7+
- **数据库连接**: SQLAlchemy, PyMySQL
- **前端**: HTML, CSS, JavaScript
- **字体支持**: SimSun (宋体) - 支持中文显示

### 系统要求

- Python 3.7+
- MySQL 5.7+
- Linux/Windows/macOS

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/longzheng268/O2O-Coupon-Feature-Analysis-and-Processing-Web.git
cd O2O-Coupon-Feature-Analysis-and-Processing-Web
```

2. **安装依赖**
```bash
pip install flask pandas matplotlib sqlalchemy pymysql numpy requests
```

3. **配置数据库**

在 `app.py` 中修改数据库连接字符串：
```python
DB_CONNECTION = 'mysql+pymysql://用户名:密码@主机:端口/数据库名'
```

创建数据库：
```sql
CREATE DATABASE O2O CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. **准备中文字体**（Linux系统）

如果在Linux系统上运行，需要准备SimSun字体文件：
```bash
# 将simsun.ttc字体文件放置到font目录
mkdir -p font
# 复制字体文件到font目录
cp /path/to/simsun.ttc font/
```

### 使用方法

1. **启动应用**
```bash
python app.py
```

应用将在 `http://0.0.0.0:5000` 启动

2. **上传数据**
   - 访问首页 `http://localhost:5000`
   - 点击"选择文件"按钮，选择CSV数据文件
   - 点击"上传"按钮开始处理

3. **查看结果**
   - 系统自动跳转到结果页面
   - 查看标签分布统计
   - 查看生成的可视化图表
   - 可选择将数据上传到数据库

### 数据格式说明

输入的CSV文件应包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| User_id | 用户ID | 1439408 |
| Merchant_id | 商户ID | 2632 |
| Coupon_id | 优惠券ID | 8591 |
| Discount_rate | 折扣率 | 20:01 或 150:20:00 |
| Distance | 距离 | 0, 1, 2, 10 |
| Date_received | 领取日期 | 20160217 |
| Date | 使用日期 | 20160613 |

### 数据库表结构

#### ccf_train_processed 表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| User_id | VARCHAR | 用户ID |
| Merchant_id | VARCHAR | 商户ID |
| Coupon_id | VARCHAR | 优惠券ID |
| Discount_rate | VARCHAR | 折扣率 |
| Distance | INT | 距离 |
| Date_received | DATETIME | 领取日期 |
| Date | DATETIME | 使用日期 |
| label | INT | 标签（1/-1/0/NULL） |

### 项目结构

```
O2O-Coupon-Feature-Analysis-and-Processing-Web/
├── app.py                  # 主应用程序文件
├── app-old.py             # 旧版本应用
├── app-new.py             # 新版本应用
├── templates/             # HTML模板
│   ├── index.html         # 首页模板
│   └── result.html        # 结果页面模板
├── static/                # 静态资源
│   ├── style.css          # 样式表
│   ├── missing_values.png # 缺失值图表
│   ├── label_distribution.png # 标签分布图
│   └── coupon_type_distribution.png # 优惠券类型分布图
├── uploads/               # 上传文件目录
├── data/                  # 数据文件目录
│   ├── ccf_train.csv      # 原始训练数据
│   ├── ccf_train_processed.csv # 处理后的数据
│   └── ccf_trainSQL脚本.SQL # SQL脚本
├── font/                  # 字体文件目录
│   └── simsun.ttc         # 宋体字体
├── docs/                  # 文档目录
│   ├── O2O优惠卷特征处理.pptx # 演示文稿
│   └── 基于MySQL的O2O优惠券特征分析处理_项目报告.docx # 项目报告
└── README.md              # 项目说明文档
```

### 核心功能说明

#### 1. 数据处理流程

```python
# 日期转换
df['Date_received'] = pd.to_datetime(df['Date_received'], format='%Y%m%d')
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

# 标签生成逻辑
# 计算领取日期和使用日期之间的天数差
days_diff = (df['Date'] - df['Date_received']).dt.days

# 标签分类：
# 1: 15天内使用优惠券
# -1: 领取但未使用
# 0: 15天后使用
# None: 其他情况
```

#### 2. 异步数据上传

系统使用多线程技术实现数据的异步上传，避免阻塞主进程：

```python
thread = threading.Thread(target=async_to_sql, args=(df, 'ccf_train_processed'))
thread.daemon = True
thread.start()
```

### 特性亮点

- ✨ **用户友好界面**：简洁直观的Web界面
- 🚀 **高效处理**：使用NumPy向量化操作，处理大规模数据
- 📊 **丰富可视化**：多种图表类型展示数据特征
- 💾 **数据持久化**：MySQL数据库存储，支持后续分析
- 🎨 **动态背景**：Bing每日壁纸自动更新
- 🌐 **跨平台支持**：支持Linux、Windows和macOS

### 许可证

本项目采用 GNU General Public License v2.0 许可证。详见 [LICENSE](LICENSE) 文件。

### 贡献

欢迎提交 Issue 和 Pull Request！

### 联系方式

- 项目主页: [GitHub Repository](https://github.com/longzheng268/O2O-Coupon-Feature-Analysis-and-Processing-Web)
- 演示视频: [YouTube](https://youtu.be/EuD5We0Vg9A)

---

## English Version

### Project Overview

This is a Flask and MySQL-based web application for O2O coupon feature analysis and processing. The system can upload, process, and analyze O2O coupon data, generate visualization charts, and store processed data in a MySQL database.

### Demo Video

📺 [Watch Demo Video](https://youtu.be/EuD5We0Vg9A)

### Key Features

1. **CSV File Upload and Processing**
   - Support for uploading raw O2O coupon data (CSV format)
   - Automatic data parsing and preprocessing

2. **Feature Engineering**
   - Date format conversion (YYYYMMDD to standard date format)
   - Automatic label generation:
     - `1`: Users who used coupons within 15 days
     - `-1`: Users who received but didn't use coupons
     - `0`: Users who used coupons after 15 days
     - `None`: Users who didn't receive coupons

3. **Data Visualization**
   - **Missing Values Chart**: Display missing value counts for each column
   - **Label Distribution Chart**: Show distribution of different label types
   - **Coupon Type Distribution**: Pie chart showing distribution of different discount rates

4. **Database Integration**
   - MySQL database integration for data persistence
   - Asynchronous data upload for improved efficiency
   - Support for data querying and export

5. **Dynamic Background**
   - Integration with Bing daily wallpaper as dynamic background
   - Automatic slideshow display

### Technology Stack

- **Backend Framework**: Flask (Python)
- **Data Processing**: Pandas, NumPy
- **Data Visualization**: Matplotlib
- **Database**: MySQL 5.7+
- **Database Connection**: SQLAlchemy, PyMySQL
- **Frontend**: HTML, CSS, JavaScript
- **Font Support**: SimSun - for Chinese character display

### System Requirements

- Python 3.7+
- MySQL 5.7+
- Linux/Windows/macOS

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/longzheng268/O2O-Coupon-Feature-Analysis-and-Processing-Web.git
cd O2O-Coupon-Feature-Analysis-and-Processing-Web
```

2. **Install Dependencies**
```bash
pip install flask pandas matplotlib sqlalchemy pymysql numpy requests
```

3. **Configure Database**

Modify the database connection string in `app.py`:
```python
DB_CONNECTION = 'mysql+pymysql://username:password@host:port/database'
```

Create the database:
```sql
CREATE DATABASE O2O CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. **Prepare Chinese Font** (Linux systems)

For Linux systems, prepare the SimSun font file:
```bash
# Place simsun.ttc font file in the font directory
mkdir -p font
# Copy font file to font directory
cp /path/to/simsun.ttc font/
```

### Usage

1. **Start Application**
```bash
python app.py
```

The application will start at `http://0.0.0.0:5000`

2. **Upload Data**
   - Visit homepage `http://localhost:5000`
   - Click "Choose File" button to select CSV data file
   - Click "Upload" button to start processing

3. **View Results**
   - System automatically redirects to results page
   - View label distribution statistics
   - View generated visualization charts
   - Optionally upload data to database

### Data Format

Input CSV file should contain the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| User_id | User ID | 1439408 |
| Merchant_id | Merchant ID | 2632 |
| Coupon_id | Coupon ID | 8591 |
| Discount_rate | Discount rate | 20:01 or 150:20:00 |
| Distance | Distance | 0, 1, 2, 10 |
| Date_received | Receive date | 20160217 |
| Date | Usage date | 20160613 |

### Database Schema

#### ccf_train_processed Table

| Field | Type | Description |
|-------|------|-------------|
| User_id | VARCHAR | User ID |
| Merchant_id | VARCHAR | Merchant ID |
| Coupon_id | VARCHAR | Coupon ID |
| Discount_rate | VARCHAR | Discount rate |
| Distance | INT | Distance |
| Date_received | DATETIME | Receive date |
| Date | Usage date |
| label | INT | Label (1/-1/0/NULL) |

### Project Structure

```
O2O-Coupon-Feature-Analysis-and-Processing-Web/
├── app.py                  # Main application file
├── app-old.py             # Old version application
├── app-new.py             # New version application
├── templates/             # HTML templates
│   ├── index.html         # Home page template
│   └── result.html        # Results page template
├── static/                # Static resources
│   ├── style.css          # Stylesheet
│   ├── missing_values.png # Missing values chart
│   ├── label_distribution.png # Label distribution chart
│   └── coupon_type_distribution.png # Coupon type distribution chart
├── uploads/               # Upload directory
├── data/                  # Data files directory
│   ├── ccf_train.csv      # Raw training data
│   ├── ccf_train_processed.csv # Processed data
│   └── ccf_trainSQL脚本.SQL # SQL script
├── font/                  # Font files directory
│   └── simsun.ttc         # SimSun font
├── docs/                  # Documentation directory
│   ├── O2O优惠卷特征处理.pptx # Presentation slides
│   └── 基于MySQL的O2O优惠券特征分析处理_项目报告.docx # Project report
└── README.md              # Project documentation
```

### Core Functionality

#### 1. Data Processing Pipeline

```python
# Date conversion
df['Date_received'] = pd.to_datetime(df['Date_received'], format='%Y%m%d')
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

# Label generation logic
# Calculate days difference between receive and usage dates
days_diff = (df['Date'] - df['Date_received']).dt.days

# Label classification:
# 1: Used within 15 days
# -1: Received but not used
# 0: Used after 15 days
# None: Other cases
```

#### 2. Asynchronous Data Upload

The system uses multi-threading for asynchronous data upload to avoid blocking the main process:

```python
thread = threading.Thread(target=async_to_sql, args=(df, 'ccf_train_processed'))
thread.daemon = True
thread.start()
```

### Highlights

- ✨ **User-Friendly Interface**: Clean and intuitive web interface
- 🚀 **Efficient Processing**: NumPy vectorization for large-scale data
- 📊 **Rich Visualization**: Multiple chart types for data insights
- 💾 **Data Persistence**: MySQL storage for further analysis
- 🎨 **Dynamic Background**: Auto-updating Bing daily wallpaper
- 🌐 **Cross-Platform**: Supports Linux, Windows, and macOS

### License

This project is licensed under the GNU General Public License v2.0. See [LICENSE](LICENSE) file for details.

### Contributing

Issues and Pull Requests are welcome!

### Contact

- Project Homepage: [GitHub Repository](https://github.com/longzheng268/O2O-Coupon-Feature-Analysis-and-Processing-Web)
- Demo Video: [YouTube](https://youtu.be/EuD5We0Vg9A)
