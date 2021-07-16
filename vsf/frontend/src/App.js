import React from 'react';
import moment from 'moment';
import { BrowserRouter } from 'react-router-dom';

import Home from './Home';

import 'antd/dist/antd.css';

moment.locale('pt-br');

const App = () => (
  <BrowserRouter>
    <Home />
  </BrowserRouter>
);

export default App;
