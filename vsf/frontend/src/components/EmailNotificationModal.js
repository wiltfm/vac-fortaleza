import React, { useState, useEffect } from 'react';
import { Form, Modal } from 'antd';
import EmailNotificationForm from '../pages/EmailNotification/EmailNotificationForm';

const EmailNotificationModal = ({ name, birth_date, visible, onOk, onCancel }) => {
  const [form] = Form.useForm();
  const [confirmLoading, setConfirmLoading] = useState(false);

  const handleSubmit = async () => {
    setConfirmLoading(true);
    try {
      const values = await form.validateFields();
      if (onOk) await onOk(values);
    } catch (error) {
      console.error('error: ', error);
    }
    setConfirmLoading(false);
  };

  useEffect(() => {
    form.resetFields();
  }, [name]);

  return (
    <Modal
      forceRender
      title="Cadastrar e-mail para Notificação"
      confirmLoading={confirmLoading}
      visible={visible}
      onOk={handleSubmit}
      onCancel={onCancel}
    >
      <EmailNotificationForm
        form={form}
        name={name}
        onEnter={handleSubmit}
        birth_date={birth_date}
      />
    </Modal>
  );
};

export default EmailNotificationModal;
