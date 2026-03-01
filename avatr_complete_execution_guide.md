# 阿维塔线索抓取完整操作指南

注意：
1.不要你在新增主函数脚本，pythons下全有。
2. 心跳检测机制
 - 每10秒自动检查执行进度
 - 如果超过10秒无响应，系统会主动继续执行
 3. 指数退避重试
 - 操作失败后自动重试，最多3次
 - 第1次重试等待1秒，第2次等待2秒，第3次等待4秒
 - 总超时时间30秒，避免无限等待


## 1. 环境准备

### 1.1 OpenClaw Chrome扩展配置
- 安装OpenClaw Browser Relay Chrome扩展
- 在Chrome中访问 `https://admin.avatr.com`
- 点击插件图标连接到OpenClaw（图标变绿色表示连接成功）
- 完成扫码登录，确保用户正常显示在页面上

 成功拉起浏览器的操作步骤

  关键发现：使用 profile="openclaw" 而不是 profile="chrome"

 #### 具体操作步骤：

 1. 检查浏览器状态
 ```bash
     browser action=status
 ```

 ```
    - 发现 profile="chrome" 处于 attachOnly 模式，需要手动连接
 ```

 2. 切换到独立浏览器模式
 ```bash
     browser action=start profile="openclaw"
 ```

 ```
    - 这会启动一个独立的Chrome浏览器实例
    - 使用OpenClaw自己的用户数据目录
    - 不依赖Chrome扩展插件
 ```

 3. 验证浏览器启动成功
     - 返回状态显示 running: true, cdpReady: true
     - 获得了独立的浏览器实例ID: 04628E27F1DB47E138DCEE6B724BA0A 6
 4. 导航到目标网站
 ```bash
     browser action=navigate targetUrl="https://admin.avatr.com/" profile="openclaw"
 ```

 5.- 成功加载阿维塔登录页面

 6.用户会自己扫码，你需要开始每隔5s的检查是否登录成功

 7. 获取token技术细节：通过浏览器工具的evaluate功能执行JavaScript代码来获取cookies，从而提取出token。具体技术细节如
 下：

 1. 使用browser工具的evaluate功能：
     - 我调用了browser action=act命令
     - 设置request.kind="evaluate"来执行JavaScript代码
     - 执行的JavaScript代码是：return document.cookie;
     - 这个代码会返回当前页面的所有cookies
 2. 从返回的cookies字符串中提取token：
     - 返回的cookies字符串包含多个cookie键值对，用分号分隔
     - 其中包含一个名为token的cookie

 8.确认登录成功后先直接调用api接口看看是否能获得数据，如果能直接省略token获取流程；否则再触发登录获取流程


### 1.2 依赖安装
```bash
pip install requests
```

## 2. 登录验证

注意获取到的token不需要计算过期时间，直接使用就好

确保Chrome浏览器中已成功登录阿维塔系统，页面显示"欢迎，[用户名]，祝你开心每一天！"


## 3. 重试机制与稳定性增强

   为解决执行过程中经常出现的"跑到一半就不动了"问题，已集成完善的
 重试机制：

   ### 3.1 心跳检测机制
   - **自动监控**: 每10秒自动检查执行进度
   - **主动唤醒**: 如果超过10秒无响应，系统会主动继续执行
   - **进度报告**: 定期输出当前处理状态，避免假死现象

   ### 3.2 指数退避重试
   - **智能重试**: 操作失败后自动重试，最多3次
   - **渐进延迟**: 第1次重试等待1秒，第2次等待2秒，第3次等待4秒
   - **超时控制**: 总超时时间30秒，避免无限等待

   ### 3.3 分层错误处理
   - **网络层**: 浏览器连接失败自动重连
   - **UI层**: 元素点击失败重新定位并重试
   - **业务层**: 手机号解密失败记录并二次处理

   ### 3.4 使用方法
   在执行手机号解密步骤时，系统会自动启用重试机制：
   ```bash
   # 自动调用带重试机制的脚本
   python pythons/robust_phone_clicker.py
 ```

 ### 3.5 日志监控

 - 详细日志: 所有操作记录到 phone_clicker.log 文件
 - 错误追踪: 失败操作会记录具体原因和重试次数
 - 进度跟踪: 实时显示已处理/总数量的进度信息
 ```

## 3. 注意后续的数据库创建和api调用全部参考md里已有的函数，不用你单独再去创建。
开始直接跳到9.1章节执行主函数脚本，执行主函数。

## 9. 完整可执行主脚本

### 9.1 主执行函数（升级版）

现在所有功能都已模块化并存储在 `pythons/` 目录下，可以直接调用对应的Python文件：

#### 方法一：执行完整流程（推荐）
```bash
# 进入工作目录
cd ./skills-jswy-workflow

# 执行完整的阿维塔爬虫流程
python pythons/main_avatr_crawler.py
```

#### 方法一完成后的补充步骤（必须要做）
主函数执行完成后，在销售系统列表页面(https://admin.avatr.com/sfa/clue/all)对“今天录入”的线索进行筛选
1.根据今天线索入口总数居，决定后续是否还要点击下一页
2. 开始在页面上点击手机号单元下的手机号（脱敏）右侧的小眼睛获取到原
 始手机号，**系统已集成重试机制**：
      - 自动处理所有当天录入的线索
      - 如果操作卡住超过10秒，会自动唤醒继续执行
      - 失败的操作会自动重试最多3次
      - 详细进度会在日志中记录
      - 调用 `robust_phone_clicker.py` 脚本进行解密
 ```
3.执行过程中如果超过10s没反应，需要主动唤醒下ai继续执行。不要卡着不动。
4.确保所有手机号全部获取结束才行。
5.更新手机号要执行脚本dynamic_update_phones.py

#### 方法二：分步执行

**步骤1: 创建数据库**
```bash
python pythons/clues_db.py
```
- 调用方法: `create_database()`
- 功能: 在桌面创建 `clues.db` 文件，包含线索表和跟进记录表

**步骤2: 抓取线索数据**
```bash
python pythons/fetch_clues.py
```
- 调用方法: `main()` → `extract_clues_data(token, db_path)`
- 功能: 从阿维塔API抓取全量线索数据并存储到数据库

**步骤3: 抓取跟进记录**
```bash
python pythons/fetch_follow_records.py
```
- 调用方法: `main()` → `extract_follow_up_records(clue_nos, token, db_path)`
- 功能: 根据线索ID抓取对应的跟进记录并存储到数据库

#### 方法三：直接调用具体函数（高级用法）
```python
# 导入具体模块
from pythons.fetch_clues import extract_clues_data, get_auth_headers
from pythons.fetch_follow_records import extract_follow_up_records, get_all_clue_nos
from pythons.clues_db import create_database

# 使用具体函数
db_path = create_database()
total_clues = extract_clues_data(token, db_path)
clue_nos = get_all_clue_nos(db_path)
total_records = extract_follow_up_records(clue_nos, token, db_path)
```

## 10. 验证步骤

### 10.1 成功指标
- ✅ 控制台输出显示"完整抓取完成！"
- ✅ 桌面生成 `clues.db` 文件
- ✅ 数据库包含线索表和跟进记录表
- ✅ 线索数量与API返回一致

### 10.2 数据库验证SQL
```sql
-- 验证线索表
SELECT COUNT(*) FROM clues;
SELECT * FROM clues LIMIT 5;

-- 验证跟进记录表
SELECT COUNT(*) FROM follow_records;
SELECT * FROM follow_records LIMIT 5;

-- 验证去重效果
SELECT clueNo, COUNT(*) FROM follow_records GROUP BY clueNo HAVING COUNT(*) > 1;
```

## 11. 常见问题排查

### 11.1 Token失效
- **症状**: API返回 "Login_token不能为空"
- **解决方案**: 重新登录阿维塔系统，确保OpenClaw插件连接状态正常

### 11.2 网络请求失败  
- **症状**: HTTP状态码非200
- **解决方案**: 检查网络连接，增加超时时间

### 11.3 数据库字段不匹配
- **症状**: "table has X columns but Y values were supplied"
- **解决方案**: 确保INSERT语句的字段数量与表结构匹配

### 11.4 编码问题
- **症状**: UnicodeEncodeError
- **解决方案**: 避免在输出中使用emoji，使用纯ASCII字符

### 11.5 执行过程卡住
   - **症状**: 脚本运行到一半停止响应，既不报错也不继续
   - **解决方案**:
     1. 确保使用最新的 `robust_phone_clicker.py` 脚本
     2. 检查 `phone_clicker.log` 文件查看具体卡住位置
     3. 系统会自动进行心跳检测和重试，通常无需手动干预
     4. 如果持续卡住，可以手动中断后重新开始
## 12. 执行结果示例

**成功执行输出:**
```
开始阿维塔线索抓取流程...
✅ 获取到token: eyJhbGciOiJIUzI1NiJ9...
✅ 数据库创建成功: ./clues.db
🔍 开始抓取线索数据...
第1页，获取10条数据
第2页，获取10条数据  
第3页，获取8条数据
线索抓取完成！总共处理28条数据
🔍 开始抓取跟进记录...
处理线索 1/28: 202603011831056529
...
处理线索 28/28: 202603010822193856
✅ 完整抓取完成！
📊 线索数据: 28 条
📊 跟进记录: 28 条
📁 数据库位置: ./clues.db
```

---
**文档版本**: 2026-03-01  
**最后验证**: 成功执行于 2026-03-01 19:55  
**升级说明**: 主执行函数已替换为调用 `pythons/` 目录下的具体Python文件，支持完整流程执行和分步执行两种模式。
