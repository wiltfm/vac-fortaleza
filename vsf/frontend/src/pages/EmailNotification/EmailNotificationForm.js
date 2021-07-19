import React, { useEffect } from 'react';
import moment from 'moment';
import { DatePicker, Form, Input } from 'antd';

const EmailNotificationForm = ({ form, name, birth_date, onEnter }) => {
  useEffect(() => {
    form.resetFields();
  }, [name, birth_date]);

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
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          name,
          birth_date: birth_date && birth_date !== '' ? moment(birth_date) : '',
        }}
      >
        <Form.Item
          label="Nome Completo (sem acento)"
          name="name"
          normalize={(value) =>
            value
              .normalize('NFD')
              .replace(/\p{Diacritic}/gu, '')
              .toUpperCase()
          }
          rules={[
            {
              required: true,
              message: 'Por favor, coloque o seu nome completo',
            },
          ]}
        >
          <Input placholder="Nome Completo (sem acento)" disabled={Boolean(name.length)} />
        </Form.Item>
        <Form.Item
          label="Data de aniversário"
          name="birth_date"
          rules={[
            {
              required: true,
              message: 'Por favor, coloque a sua data de aniversário',
            },
          ]}
        >
          <DatePicker disabled={Boolean(name.length)} style={{ width: 200 }} format="DD/MM/YYYY" />
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
