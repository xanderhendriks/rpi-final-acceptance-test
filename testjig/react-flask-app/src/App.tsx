import React, { useState, useEffect } from 'react';
import { Row, Col, Container } from 'react-bootstrap';
import { LogWindow, Header, Sidebar } from 'components';
import { RunTests, SessionDetails } from 'pages';

import styled from '@emotion/styled';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const Wrapper = styled.div`
  height: 100vh;
  display: flex;
  flex-direction: column;
`;

const FillRow = styled(Row)`
  flex: 1;
`;

function App() {
  const [logs, setLogs] = useState<string[]>([]);
  const [currentTab, setCurrentTab] = useState(0);
  const [operatorName, setOperatorName] = useState('');

  useEffect(() => {
    const source = new EventSource("http://" + window.location.hostname + ":5000/stream");

    source.addEventListener('message', handleRedisMessage, false);
    source.addEventListener('error', handleRedisError, false);

    return () => {
      source.removeEventListener('message', handleRedisMessage, false);
      source.removeEventListener('error', handleRedisError, false);
    };
  }, []);


  return (
    <Wrapper>
      <Container
        style={{ display: 'flex', flexDirection: 'column', height: '100%' }}
      >
        <Header />
        <FillRow>
          <Col sm={true} lg={3}>
            <Sidebar
              activeStep={currentTab}
              setCurrentTab={setCurrentTab}
            />
          </Col>
          <Col sm={true}>
            {currentTab === 0 ? (
              <SessionDetails
                name={operatorName}
                setName={setOperatorName}
              />
            ) : null}
            {currentTab === 1 ? (
              <RunTests
                operatorName={operatorName}
              />
            ) : null}
          </Col>
        </FillRow>
        <Row>
          <LogWindow log={logs} />
        </Row>
      </Container>
    </Wrapper>
  );

  function handleRedisMessage(event: any) {
    const data = JSON.parse(event.data);
    console.log(data.message);
    setLogs(logs => [...logs, data.message]);
  }

  function handleRedisError(event: any) {
    console.log('Error', event);
    setLogs(logs => [
      ...logs,
      'Failed to connect to event stream. Is Redis running?'
    ]);
  }
}

export default App;
