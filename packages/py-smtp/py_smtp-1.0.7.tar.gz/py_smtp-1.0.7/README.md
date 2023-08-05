# 邮件发送

## 使用说明

```python
from py_smtp import send

send('smtp服务器', 465,['测试员', 'wujh@ebfcn.com.cn'], '密码', ['收件人1','收件人2'], ['抄送人1','抄送人2'], '标题', '内容', ['附件1','附件2'])
```
