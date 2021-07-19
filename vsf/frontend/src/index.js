import React from 'react';
import moment from 'moment';
import 'moment/locale/pt-br';
import { ConfigProvider } from 'antd';
import ptBR from 'antd/lib/locale/pt_BR';
import { render } from 'react-dom';
import App from './App';

moment.locale('pt-br');

render(
  <ConfigProvider locale={ptBR}>
    <App />
  </ConfigProvider>,
  document.getElementById('root')
);
