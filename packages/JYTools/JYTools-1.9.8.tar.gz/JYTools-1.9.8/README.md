Tools
jingyun tools

## 1.9.8
打卡时判断is_running

## 1.9.7
fix bug redisworker params为string时 解析数据错误

## 1.9.6
CacheRedis 添加方法setex2
修复BUG DAG当调用fail_pipeline时当不直接将任务置成error时有些未return

## 1.9.5
add CacheRedis

## 1.9.3
MyEmail support send attachment

## 1.9.2
fix bug. bug is 任务失败没有计算 Queue 的任务数量
DAG support sub_task_detail as task_list
fix bug. 修复BUG 。 当pipeline结构中包含task_output 且key和output_*重复，写警告日志错误的BUG
DAG 自动保存fail掉的任务详情时 保存的文件名加入时间戳，防止被覆盖

## 1.9.1
update DAGTools
format pipeline not save task_output
DAG more warning log

## 1.9.0
Worker execute_subprocess add out_file
execute_subprocess支持倒数第二为> 最后一个参数为标准输出的文件路径

## 1.8.8
WorkerTask add _auto_report auto_report
当auto_report为True 可汇报


## 1.8.7
可以从JYTools.JYWorker 引用TaskType

## 1.8.6
RedisWorker Add push_control
DAG Worker 接收到STOP命令，将控制传递给子任务

## 1.8.4
修复BUG pipeline任务并行时 出现提前fail pipeline

## 1.8.3
test时允许单独指定report_scene
worker_run 支持--report-scene
runtime作为task信息标准参数

## 1.8.2
DAG 支持汇报runtime信息

## 1.8.1
修复一代数据格式处理问题(未将report任务标记出来)

## 1.8.0
整理汇报处理逻辑
允许放入的任务信息里包含task_name
repeat-app拆分成多个并行任务时可使用同一个task_name

## 1.7.9
WorkerTaskParams 获取key的值时会调用debug_func。防止调用多次，一个key只允许调用一次
减少合并DAG调度中的日志

## 1.7.8
add StringEscape
add package_task_v2 unpack_task_v2
DAG Worker 可以处理stop信号
add jyworker.delete-dirty-item

## 1.7.7
fix DAG fail not report

## 1.7.5
DAG 自动保存fail掉的任务详情

## 1.7.4
report-task 可以设置task_output

## 1.7.2
worker启动后可处理系统信号 signal.SIGINT signal.SIGTERM signal.SIGUSR1 signal.SIGUSR2,如有任务将任务重新放入延时队列
DAGWorker防止重新汇报 只允许Running状态下可以多次汇报
记录 尝试去获得任务的次数（无论是否获得数据，无论从哪个队列中获得） num_pop_task
支持接收控制任务
add util/file 写文件

## 1.6.7
worker启动时默认发送一个空包清洗旧的worker

## 1.6.6
DAG放入调度的KEY 不允许与正在调度的KEY一样

## 1.6.4
DAG调度支持实时汇报

## 1.5.5
add jyworker.report-task

## 1.5.3
add jyworker.push-task

## 1.5.2
pipeline调度时检查pipeline结构，但仅做参考
pipeline发现子任务所有参数就绪时，设置状态为Ready（原来为Running）

## 1.5.0
ReadWorkerLog返回日志可设置最多读取多少日志（不是返回多少日志）

## 1.4.7
pipeline调度时，子任务的输入无法满足时（引用不存在等），同时将子任务的状态置成FAIL

## 1.4.6
WorkerLogConfig add origin_log_dir

## 1.4.5
fix TaskStatus判断None状态时报错

## 1.4.4
解决debug模式下 不能将信息打印到标准输出

## 1.4.3
解决DAGTools不能打印警告信息问题
更新DAGTools的验证顺序

## 1.4.2
RedisQueue add push_file
TaskStatus add is_success is_running is_fail
add DAGTools
add jyworker.dag-verify

## 1.4.1
add jyworker.look-item

## 1.3.9
EmailManager 去除debug

## 1.3.8
EmailManger 通过ssl服务器发送邮件

## 1.3.7
DAG worker 支持 输入 引用时最后加上*，表示为非必须引用，若引用不到，则不将该输入传给任务
jyworker.wash-worker support -a/--auto

## 1.3.6
jyworker.wash-worker 支持一次清洗多个

## 1.3.4
jyworekr.del-heartbeat 支持一次删除多个

## 1.3.3
DAG参数引用格式更改, 最后可以加入*结尾，也可以不加入，暂时定义为required

## 1.3.2
fix not print
print change to logging.debug

## 1.3.1
add jyworker.stop-worker jyworker.del-heartbeat

## 1.2.6
JYTools.JYWorker.DAG清理任务属性时 打印日志
JYTools.DB 改为使用myqldb_rich中的DB
JYTools.JYFlask 改为使用flask_helper中的

## 1.2.5
fix JYTools.JYWorker.DAG 启动问题

## 1.2.4
JYTools.JYWorker worker_run方法

## 1.2.3
fix RedisWorker parse_args解析-D --daemon bug

## 1.2.2
fix RedisWorker test时初始化任务sub_key report_tag bug

##1.2.1
DAGWorker支持Agent Push Task
RedisWorker增加方法parse_args解析命令行参数

## 1.1.9
fix not write log in debug mode

## 1.1.8
WorkerTask增加属性log_path记录日志位置
fix DAG task_status bug
add UploadLogWorker

## 1.1.7
WorkerTask增加属性task_errors用于记录任务多条错误信息
DAGWorker 发现错误时，立刻将pipeline的状态置成Fail
DAGWorker 发现当前Pipeline状态为Fail时，终止调度返回
调整RedisWorker 运行起来后才设置心跳值
WorkerConfig WorkerTaskParams add __slots__
RedisStat 添加方法 remove_queue_task
从WorkerConfig移出一些变量到Worker
如果任务设置error_continue不为True Pipeline有任务失败时，尝试删除已放入队列的任务

## 1.1.6
fix bug DAG Worker引用其他任务的输出时，输出值为list时，list的每一个元素都不能是以&开头的字符串

## 1.1.5
RedisWorker构造函数，增加is_brother参数，此参数为true时，优先使用现有的心跳值
RedisStat 添加方法 delete_heartbeat
fix bug DAG Worker

## 1.1.4
DAG调度，只要有任务汇报结果为Fail，就写入ERROR日志

## 1.1.3
DAG任务调度，RepeatApp的所有输入都不是list的时候，所有输入都转成包含一个元素的list
ReadWorkerLog，可查询以sub_key_prefix为前缀的sub_key
RedisStat 添加方法 list_worry_queue

## 1.1.2
DAG任务调度，支持RepeatApp的输入list的长度不一致，但长度都必须能整除最大长度
DAG任务调度，支持RepeatApp输出设置成&&+数字开头的key或& + 任意数字 + &+数字开头的key

## 1.1.1
DAG任务调度，子任务失败后打印出sub_key 以及work_tag

## 1.0.10
解决ReadWorkerLog当sub_key设置为空字符串时读取日志时BUG

## 1.0.9
修改日志中的级别用词，将WARING替换为WARNING

## 1.0.8
fix RedisWorker在daemon运行下不能打卡的问题

## 1.0.7
ReadWorkerLog添加注释
写入运行时间和开始汇报，日志级别由INFO改成DEBUG
RedisStat 添加方法 list_heartbeat list_heartbeat_detail

## 1.0.6
ReadWorkerLog 查询的level为小写时自动转为大写

## 1.0.5
set_output的日志级别由INFO变为DEBUG

## 1.0.4
StringTools 添加方法 join_decode join_encode
JYWorker添加类ReadWorkerLog

## 1.0.3
RedisWorker 添加方法 has_task_item

## 1.0.2
DAGWorker 引用支持key以数字开头
StringTools 添加方法 m_print
fix JYWorker task log bug in debug module

## 1.0.1
JYWorker添加方法sub_classes，获得所有最后的RedisClass的子类

## 0.9.11
worker运行时 增加打印clock_key

## 0.9.9
只要params是dict类型都转换成WorkerTaskParams类型

## 0.9.8
RedisStat 增加 list_queue_detail
fix DAGWorker bug

## 0.9.7
RedisStat 增加 list_worker list_worker_detail

## 0.9.5
增加requires six

## 0.9.4
fix find_loop bug

## 0.9.3
DAGWorker update function find_loop. old find_loop move to find_loop2

## 0.9.1
修改不适合python3的代码，使得代码既符合python3又符合python2
DAGWorker 增加方法exist_loop find_loop 判断是否有回路和获得回路

## 0.8.11
DB execute_select 加入参数prefix_value 支持按前缀查找

## 0.8.10
test 时默认进入debug模式
执行完成后，由原先的只返回task_output该为返回task_status,task_output

## 0.8.9
fix bug: hang_up_clock test模式下sleep死循环

## 0.8.7
开发JYTools中JYWorker交互式生成配置文件

## 0.8.6
task信息全部转成unicode

## 0.8.5
fix bug: test方法return时AttributeError: 'NoneType' object has no attribute 'task_output'

## 0.8.4
fix bug: hang_up_clock debug模式下sleep死循环

## 0.8.3
fix bug: 解决task_log中publish_message时task_key中文问题

## 0.8.2
fix bug


## 0.7.11
RedisWorkerConfig类增加静态方法write_config,可以根据参数生成配置文件
