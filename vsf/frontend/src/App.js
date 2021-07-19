import React from 'react';
import { BrowserRouter } from 'react-router-dom';

import Home from './Home';

import 'antd/dist/antd.css';

const App = () => (
  <BrowserRouter>
    <Home />
  </BrowserRouter>
);

export default App;
