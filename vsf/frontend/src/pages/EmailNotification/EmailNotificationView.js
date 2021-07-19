import React, { useState } from 'react';
import { Button, Card, Form } from 'antd';
import EmailNotificationForm from './EmailNotificationForm';
import { saveEmailNotification } from '../../services/Api';

const EmailNotificationView = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const values = await form.validateFields();
      await saveEmailNotification(values);
    } catch (error) {
      console.error('error: ', error);
    }
    setLoading(false);
  };

  return (
    <div>
      <Card>
        <EmailNotificationForm form={form} name="" birth_date="" onEnter={handleSubmit} />
        <Button type="primary" onClick={handleSubmit} loading={loading}>
          Me Notificar
        </Button>
      </Card>
    </div>
  );
};

export default EmailNotificationView;
