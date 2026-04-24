# CDP对接UQPay API操作反馈

**文档说明：** CDP对接UQPay API的详细操作反馈，包含各模块的具体操作流程和注意事项。

---

## 一、预定卡片

- **操作方式：** 线下操作，由UQpay专人负责
- **数量限制：** 单批次在10,000张卡以下
- **交货时间：** 
  - 有库存：约1周
  - 无库存：4-6周
  - 建议提前沟通采购需求
- **卡号传输：** 卡号生成后由双方约定的加密方式传输，由CDP录入卡片管理系统以记录并对应未来的持卡人
- **传输方式：** 目前以加密邮件方式发送到指定邮箱

---

## 二、建立持卡人

### API操作上传三要素信息
- 持卡人姓名
- 手机号码
- 邮箱

### 重要提示
- **邮箱很重要**：是未来接受验证码等信息的唯一通路
- 持卡人姓名和手机号码常规即可，仅需要对应到CDP的CRM系统

---

## 三、分配卡片、卡片激活

1. CDP收到建立持卡人API的回应后
2. 由CDP按照自己方式设定卡号分配
3. 同时按CRM管理让持卡人设置6位密码
4. 卡片和激活信息通过API上传
5. 回应后卡片即完成激活

---

## 四、卡片分配金额

### 操作方式
- CDP通过API更新持卡人来分配金额到持卡人卡片
- 使用 `update card/recharge` 接口更新

### 查询接口
- **卡片可用余额：** https://developers.uqpay.com/card-issuance/v1.6/api-reference/retrieve-card#response-available-balance
- **发卡账户可用余额：** https://developers.uqpay.com/card-issuance/v1.6/api-reference/list-issuing-balances#response-data-items-available-balance

---

## 五、交易提醒

### Webhook通知
- UQpay的webhook会跟CDP API互动来提醒每一笔交易
- 信息包括：持卡人ID、交易时间、交易商户、交易金额、交易状态

### CDP处理
- CDP获取信息后计入CRM系统
- 用来更新持卡人余额查询、交易查询

### 余额计算公式
```
交易余额 = 开卡以来卡片分配金额汇总额 - 查询时间点前成功交易汇总额
```

---

## 六、3DS/OTP确认

### 典型场景
- 第一次在某个网站使用该卡
- 单笔交易金额大于$400

### 邮件通知选项
1. **选项一：** 由UQpay代表CDP给客户发邮件通知（推荐）
2. **选项二：** 由CDP自己给持卡人发送邮件通知

### 重要提示
- 如果CDP选择自己发送邮件，那么UQ不会给持卡人发送任何邮件（包括3DS OTP）
- 需要CDP根据webhook通知自己处理

---

## 七、卡片冻结或者解冻

### 操作流程
- **冻结：** 持卡人发起暂时冻结该卡片交易
- **解冻：** 持卡人发起解冻该卡片交易

### API操作
- 由CDP通过API操作 `frozen/unfrozen`

---

## 八、锁卡及解锁

### 锁卡触发
- 由UQpay的风控规则发起
- 持卡人会通过webhook的交易提醒后在CDP系统里发现

### 通知方式
- 通过 `card state update` 通知

### 解锁流程
1. CDP线下通过UQpay或UQpay的客服来跟客户确认
2. 由CDP发起解锁申请

### 邮件申请格式
```
邮件标题：Card Unblock Request

邮件内容：
- card holder name
- card id
- current status: Blocked
- reason for request：[简要说明，如"误操作导致锁定"或"使用权限恢复"等]
```

---

## 九、入账差错调整

### 典型场景
客户卡片月入账出现差额

### 调整方式
1. **方式一：** 通过withdraw方式单独调整
2. **方式二：** 管理员通知UQpay后台调节

### 持卡人更换卡片时的处理
1. 在需要挪出余额的卡片做withdraw交易
2. 使用 `update card` 接口更新到新卡
3. 同时CDP发起 `pre cancel` 动作
4. 旧卡30天后自动取消

---

## 十、其他注意事项

### API文档参考
- 完整API文档：https://developers.uqpay.com/card-issuance/v1.6/

### 联系方式
- 技术支持邮箱：support@uqpay.com

---

**文档整理：** 知识库管家清越  
**整理日期：** 2026-04-14
