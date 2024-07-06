import React, { useState } from 'react';
import styled from '@emotion/styled';
import { Button } from 'react-bootstrap';

const Container = styled.div`
    display: flex;
    flex-direction: column;
    flex: 1;
    height: 100%;
`
const TestReport = styled.iframe`
  flex: 1;
`

interface Props {
  operatorName: string;
}

function RunTests({ operatorName }: Props) {
  const [reportGenerated,setReportGenerated] = useState<boolean>(false);
  const [serialNumber, setSerialNumber] = useState('');
  const [boardSerialNumber, setBoardSerialNumber] = useState<string>(``);

  const handleRunTestsClick = async () => {
      await fetch('/api/test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
                    boardSerialNumber: boardSerialNumber,
                    operatorName: operatorName,
                }),
    })
      .then(res => res.json())
      .then((data: { status: string; report_filename: string }) => {
        console.log('TEST', data, data.status === 'OK');

        if (data.status === 'OK' || data.status === 'TESTS_FAILED' || data.status === 'INTERRUPTED') {
          setReportGenerated(true);
        }
      })
      .catch(error => {
        console.error('Error during test run:', error);
      });
  };

  const handleSerialNumberChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = event.target.value;
    setSerialNumber(inputValue);
    setBoardSerialNumber(`${inputValue}`);
  };

  console.log('render logs', reportGenerated, window.location.hostname);

  return (
    <Container>
      <h1>Automated Tests</h1>
      <div>
        <label>
          Serial number:
          <input
              type="text"
              value={serialNumber}
              placeholder={"XXXXXXXXXX"}
              onChange={handleSerialNumberChange}
          />
        </label>
        {serialNumber.length !== 10 && (
          <p style={{ color: 'red' }}>End of serial number must be 10 digits</p>
        )}
      </div>
      <Button style={{ marginTop: '10px' }} onClick={handleRunTestsClick}>Run tests</Button>
      {reportGenerated && <TestReport src={`http://${window.location.hostname}:5000/api/test-report/${boardSerialNumber}`} />}
    </Container>
  );
}

export default RunTests;
