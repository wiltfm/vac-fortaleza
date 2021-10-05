import React, { useState } from 'react';
import { Button, Card, Drawer, Grid } from 'antd';
import { MenuOutlined } from '@ant-design/icons';

import Router from './Router';
import AppMenu from './components/Menu';
import SheetsMarquee from './components/SheetsMarquee';

const { useBreakpoint } = Grid;

const Home = () => {
  const [visible, setVisible] = useState(false);

  const screens = useBreakpoint();
  const md = !!screens.md;

  const BtnExtra = () => {
    if (md) return null;
    return <Button type="primary" icon={<MenuOutlined />} onClick={() => setVisible(true)} />;
  };

  return (
    <div style={{ padding: 20 }}>
      <Card title="Vacina contra Covid-19 Fortaleza" extra={<BtnExtra />}>
        <div>
          Olha se seu nome saiu na lista de agendamento da vacina{' '}
          <a
            href="https://coronavirus.fortaleza.ce.gov.br/lista-vacinacao-d1.html"
            target="_blank"
            rel="noreferrer"
          >
            divulgada pela Prefeitura de Fortaleza
          </a>
          <br />
          Aqui você pode cadastrar seu email para receber uma notificação assim que a gente souber
          que seu nome está na lista
        </div>
      </Card>
      {md ? (
        <AppMenu />
      ) : (
        <Drawer
          title="Menu"
          placement="right"
          closable={false}
          onClose={() => {
            setVisible(false);
          }}
          visible={visible}
        >
          <AppMenu
            mode="vertical"
            onClick={() => {
              setVisible(false);
            }}
          />
        </Drawer>
      )}
      <div style={{ paddingTop: 16 }}>
        <Router />
      </div>
      <SheetsMarquee />
    </div>
  );
};

export default Home;
