import React from 'react';
import { Col, Row } from 'react-bootstrap';
import styled from '@emotion/styled';

// Define a styled Row with rounded corners
const StyledRow = styled(Row)`
  border-radius: 8px;
`;

function Header() {
  return (
    <StyledRow className="p-3 mb-2 bg-primary text-white">
      <Col>
        <img src="/logo.png" alt="Logo" height={25} />
      </Col>
      <Col>Workshop Test Jig</Col>
      <Col>[{window.location.hostname}]</Col>
    </StyledRow>
  );
}

export default Header;
