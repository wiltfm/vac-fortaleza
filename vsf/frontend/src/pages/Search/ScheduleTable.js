import React, { useState } from 'react';
import moment from 'moment';
import { Table } from 'antd';
import ScheduleTableBtns from './ScheduleTableBtns';
import EmailNotificationModal from '../../components/EmailNotificationModal';
import { saveEmailNotification } from '../../services/Api';

const ScheduleTable = (props) => {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalName, setModalName] = useState('');

  const onEmailClicked = (schedule) => {
    setModalVisible(true);
    setModalName(schedule.name);
  };

  const onOk = async (values) => {
    await saveEmailNotification(values);
    setModalVisible(false);
  };

  const columns = [
    {
      title: 'Nome',
      dataIndex: 'name',
    },
    {
      title: 'Aniversário',
      dataIndex: 'birth_date',
      render: (value) => moment(value).format('L'),
      responsive: ['md'],
    },
    {
      title: 'Dose',
      dataIndex: 'dose',
    },
    {
      title: 'Data',
      dataIndex: 'date',
      render: (value) => moment(value).format('DD/MM/YYYY HH:mm'),
    },
    {
      title: 'Lugar',
      dataIndex: 'place',
      responsive: ['sm'],
    },
    {
      render: (_, record) => (
        <ScheduleTableBtns schedule={record} onEmailClicked={() => onEmailClicked(record)} />
      ),
    },
  ];
  return (
    <>
      <Table {...props} columns={columns} rowKey="id" />
      <EmailNotificationModal
        visible={modalVisible}
        name={modalName}
        onOk={onOk}
        onCancel={() => setModalVisible(false)}
      />
    </>
  );
};

export default ScheduleTable;
