import React from 'react';
import moment from 'moment';
import { Button, Descriptions, Divider, Grid, Modal } from 'antd';
import { MailOutlined, InfoCircleOutlined } from '@ant-design/icons';

const { useBreakpoint } = Grid;

const ScheduleTableBtns = ({ schedule, onEmailClicked }) => {
  const screens = useBreakpoint();
  const sm = !!screens.sm;

  const openInfoModal = () => {
    Modal.info({
      title: 'Detalhes Agendamento Vacina contra Covid-19',
      width: '100%',
      content: (
        <div>
          <Descriptions>
            <Descriptions.Item label="Nome">{schedule.name}</Descriptions.Item>
            <Descriptions.Item label="Aniversário">
              {moment(schedule.birth_date).format('L')}
            </Descriptions.Item>
            <Descriptions.Item label="Data Agendamento">
              {moment(schedule.date).format('LLL')}
            </Descriptions.Item>
            <Descriptions.Item label="Lugar">{schedule.place}</Descriptions.Item>
            <Descriptions.Item label="Dose">{schedule.dose}</Descriptions.Item>
            <Descriptions.Item label="Arquivo">
              <a href={schedule.spreadsheet.url}>{schedule.spreadsheet.name}</a>
            </Descriptions.Item>
            <Descriptions.Item label="Página">{schedule.spreadsheet_page}</Descriptions.Item>
            <Descriptions.Item label="Linha">{schedule.spreadsheet_line}</Descriptions.Item>
          </Descriptions>
        </div>
      ),
      onOk() {},
    });
  };

  return (
    <div style={sm ? { display: 'flex' } : {}}>
      <Button shape="circle" icon={<InfoCircleOutlined />} onClick={openInfoModal} />
      <Divider type={sm ? 'vertical' : 'horizontal'} />
      <Button type="primary" shape="circle" icon={<MailOutlined />} onClick={onEmailClicked} />
    </div>
  );
};

export default ScheduleTableBtns;
