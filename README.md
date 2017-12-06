# teaching

Tasks of teaching repo for zoumeng

zoumeng的任务笔记

## TODO List

### 任务一：学校学生管理系统

完成学校学生管理系统。学校存在多个班级，可以通过页面进行学生信息的展示、注册学生信息。

学生展示页面需求：

1. 全体学生展示。（先完成，后期希望能够用到Vue进行展示）

2. 某个班级学生展示。

3. 通过搜索某一个学生展示特定学生。


有下面几个模块组成：

1. 前端页面服务，用户可以通过界面进行管理和展示

2. 使用python flask提供一个web service, 提供Restful API，对页面请求作出相应的处理

3. 用MySQL数据库，管理学生数据信息。docker服务模式，使用Python SQLAlchemy对数据库进行管理