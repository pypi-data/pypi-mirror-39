# SQLAlchemy_wrap
对SQLAlchemy的简单封装,支持查找指定文件夹中的类(目前是一个表对应一个类).
* 对[SQLAlchemy](https://docs.sqlalchemy.org/en/latest/)的封装,支持查找指定文件夹中的数据库操作类(暂时只考虑单表操作)
* 使用自定义基类直接操作数据库,基类包含基础的增删查改的方法
* 可以直接使用已有库,也可以在继承类中使用建库语法进行建库并对应操作
* 个人喜欢搭配工厂模式去使用,很舒服
* 可以使用建表语句去建立新表,也可以使用原有的表
# example
见 `example` 目录下的demo.

这里说下指定文件夹的想法.
```
--database
  |__db1
  |   |___ table1.py
  |   |___ table2.py
  |___db2
      |___ table3.py
      ......
```
比如我们数据库(sqlite)下有 `db1` 和 `db2` 两个库, `db1` 有 `table1`,`table2` 两个表, `db2` 有 `table3` 表, 这样我们就可以指定`table1.py`去对应
`db1.table1` 的表操作了.

# 关于SQLAlchemy
* 在基类`BaseTable`中保留了两个指针 `self.engine` 对应 `SqlAlchemy.create_engine`对象, 以及 `self.table` 对应 `SqlAlchemy.table` 对象. 你可以使用这两个中的一个去进行各种orm操作
