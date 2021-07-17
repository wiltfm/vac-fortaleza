import React, { useState, useEffect } from 'react';
import { Button, Input, Row, Col } from 'antd';
import ScheduleTable from './ScheduleTable';
import { getSchedules } from '../../services/Api';

const SearchView = () => {
  // const [name, setName] = useState('');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [schedules, setSchedules] = useState([]);

  const setSearchValue = (value) => setSearch(value.normalize('NFD').replace(/[\u0300-\u036f]/g, ''));

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') setSearchValue();
  };

  useEffect(() => {
    const asyncSearchSchedules = async () => {
      setLoading(true);
      try {
        const response = await getSchedules(search);
        const data = await response.json();
        setSchedules(data.results);
      } catch (error) {
        console.log(error);
      }
      setLoading(false);
    };

    if (search === '') {
      setSchedules([]);
    } else {
      asyncSearchSchedules();
    }
  }, [search]);

  return (
    <>
      <Row wrap={false} style={{ alignItems: 'center' }}>
        <Col flex="auto">
          <Input.Search
            placeholder="Nome"
            // onChange={(e) => setName(e.target.value)}
            onKeyDown={handleKeyDown}
            enterButton={true}
            loading={loading}
            onSearch={setSearchValue}
          />
        </Col>
      </Row>
      <ScheduleTable loading={loading} dataSource={schedules} />
    </>
  );
};

export default SearchView;
