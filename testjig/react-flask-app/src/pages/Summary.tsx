import React from 'react';
import { Button } from 'react-bootstrap';

interface Props {
  reset: () => void;
  submit: () => void;
}

function Summary({ reset, submit }: Props) {
  return (
    <div>
      <h1>Done!</h1>
      <Button onClick={submit}>Download CSV</Button>
      <Button onClick={reset}>Reset</Button>
    </div>
  );
}

export default Summary;
