import React, { useEffect } from 'react';
import { Form, Input } from 'antd';

const EmailNotificationForm = ({ form, name, onEnter }) => {
  useEffect(() => {
    form.resetFields();
  }, [name]);

  const handleKeyDown = async (event) => {
    if (onEnter && event.key === 'Enter') {
      onEnter();
    }
  };

  return (
    <div>
      <p>
        Assim que a gente identificar o nome, vamos te enviar um email com os dados do agendamento.
        <br />
        Vai servir como mais um lembrete, mas não esquece de verificar no{' '}
        <a
          target="_blank"
          href="https://coronavirus.fortaleza.ce.gov.br/lista-vacinacao-d1.html"
          rel="noreferrer"
        >
          site oficial da prefeitura.
        </a>
      </p>
      <Form form={form} layout="vertical" initialValues={{ name }}>
        <Form.Item
          label="Nome"
          name="name"
          rules={[
            {
              required: true,
              message: 'Por favor, coloca o seu nome completo',
            },
          ]}
        >
          <Input disabled={Boolean(name.length)} />
        </Form.Item>
        <Form.Item
          label="Email"
          name="email"
          rules={[
            { required: true, message: 'Por favor, coloque seu email' },
            { type: 'email', message: 'Formato de email inválido' },
          ]}
        >
          <Input placeholder="email" onKeyDown={handleKeyDown} />
        </Form.Item>
      </Form>
    </div>
  );
};

export default EmailNotificationForm;
