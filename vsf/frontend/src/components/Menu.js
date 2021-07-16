import React from 'react';
import { Menu } from 'antd';
import {
  AreaChartOutlined,
  InfoCircleOutlined,
  MailOutlined,
  SearchOutlined,
} from '@ant-design/icons';
import { Link, useLocation } from 'react-router-dom';

import { RouterKeys } from '../Router';

const AppMenu = ({ mode = 'horizontal', onClick = null }) => {
  const location = useLocation();
  const defaultKey = Object.values(RouterKeys).includes(location.pathname)
    ? location.pathname
    : RouterKeys.search;

  return (
    <Menu
      defaultSelectedKeys={[defaultKey]}
      mode={mode}
      onClick={(value) => onClick && onClick(value)}
    >
      <Menu.Item key={RouterKeys.search} icon={<SearchOutlined />}>
        <Link to={RouterKeys.search}>Busca</Link>
      </Menu.Item>
      <Menu.Item key={RouterKeys.notification} icon={<MailOutlined />}>
        <Link to={RouterKeys.notification}>Notificação</Link>
      </Menu.Item>
      <Menu.Item key={RouterKeys.stats} icon={<AreaChartOutlined />}>
        <Link to={RouterKeys.stats}>Estatística</Link>
      </Menu.Item>
      <Menu.Item key={RouterKeys.about} icon={<InfoCircleOutlined />}>
        <Link to={RouterKeys.about}>Sobre</Link>
      </Menu.Item>
    </Menu>
  );
};

export default AppMenu;
