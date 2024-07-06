import React from 'react';
import { Form } from 'react-bootstrap';

interface Props {
  name: string;
  setName: (name: string) => void;
}

function SessionDetails({ name, setName }: Props) {
  return (
    <div>
      <h1>Session Details</h1>
      <Form>
        <Form.Group controlId="formBasicName">
          <Form.Label>Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter name"
            value={name}
            onChange={e => setName(e.target.value)}
          />
        </Form.Group>
      </Form>
    </div>
  );
}

export default SessionDetails;
