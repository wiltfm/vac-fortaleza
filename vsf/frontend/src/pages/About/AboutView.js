import React from 'react';
import { Card } from 'antd';
import { GithubOutlined, TwitterOutlined, LinkedinOutlined } from '@ant-design/icons';

const AboutView = () => (
  <Card
    actions={[
      <a href="https://github.com/wilkmoura/" target="_blank" rel="noreferrer" key="git">
        <GithubOutlined style={{ fontSize: '24px', color: '#333' }} />
      </a>,
      <a href="https://twitter.com/wilkmoura" target="_blank" rel="noreferrer" key="twi">
        <TwitterOutlined style={{ fontSize: '24px', color: '#1DA1F2' }} />
      </a>,
      <a
        href="https://www.linkedin.com/in/wilkinson-tavares/"
        target="_blank"
        rel="noreferrer"
        key="lin"
      >
        <LinkedinOutlined style={{ fontSize: '24px', color: '#0A66C2' }} />
      </a>,
    ]}
  >
    Fiz esse projeto para aprender um pouco sobre docker e docker-compose.
    <br />
    <a href="/api/" target="_blank" rel="noreferrer">
      Para consumir a API REST.
    </a>
    <br />
    <a href="https://github.com/wilkmoura/vac-fortaleza" target="_blank" rel="noreferrer">
      Se quiser contribuir é só mandar um PR no github.
    </a>
    <br />
    <br />
    Se vacine, se proteja, usa máscara e proteja os outros.
    <h3>Viva o SUS!</h3>
  </Card>
);

export default AboutView;
