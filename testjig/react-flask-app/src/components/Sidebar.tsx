import React, { useState } from 'react';
import styled from '@emotion/styled';
import {Button} from 'react-bootstrap';
import {
    CheckmarkIcon,
    CircleIcon,
    LeftChevronIcon,
    RightChevronIcon
} from 'components/Icons';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  flex: 1;
  height: 100%;
  background: rgba(var(--bs-primary-rgb));
  color: white;
  border-radius: 8px;
`;

const Title = styled.h3`
  text-align: center;
  margin-bottom: 20px;
  padding: 8px;
`;

const Filler = styled.div`
  flex: 1;
`;

const Body = styled.div`
  position: relative;
`;

const StyledButton = styled(Button)`
  display: flex;
  align-items: center;
`;

const Row = styled.div<{ active: boolean; complete: boolean }>`
  display: flex;
  gap: 4px;
  padding: 4px;
  font-weight: ${({active}) => (active ? 'bold' : 'default')};
  color: white;
  border-bottom: 1px solid black;
  height: 30px;
  align-items: center;
  z-index: 2;
`;

const Footer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 4px;
  padding: 4px;
`;

const StepStatus = ({complete}: { active: boolean; complete: boolean }) =>
    complete ? <CheckmarkIcon/> : <CircleIcon/>;

const Step = ({
                  stepIndex,
                  currentStep,
                  children
              }: {
    stepIndex: number;
    currentStep: number;
    children: React.ReactNode;
}) => (
    <Row active={currentStep === stepIndex} complete={currentStep > stepIndex}>
        <StepStatus
            active={currentStep === stepIndex}
            complete={currentStep > stepIndex}
        />
        {children}
    </Row>
);

const SETUP_STEPS = ['Session Details', 'Automated Tests'];

interface Props {
    activeStep?: number;
    setCurrentTab: (tab: number) => void;
}

function Sidebar({setCurrentTab, activeStep = 1}: Props) {
    const [isLoading, setIsLoading] = useState(false);

    const handleNextButtonClick = async () => {
        // If on last page, the next button navigates back to the first page
        if (activeStep === SETUP_STEPS.length - 1) {
            setCurrentTab(1);
        } else {
            if (activeStep === 2) {
                setIsLoading(true);
                try {
                    const response = await fetch('/api/initial-test', {
                        method: 'GET',
                    });
                    if (response.ok) {
                        console.log('Initial test successful.');
                    } else {
                        console.error('Failed to run initial test.');
                    }
                } catch (error) {
                    console.error('Error during initial test:', error);
                } finally {
                    setIsLoading(false);
                }
            }

            // Set the current tab to the next page
            setCurrentTab(activeStep + 1);
        }

    };


    return (
        <Container>
            <Title>Setup steps</Title>
            <Filler>
                <Body>
                    {SETUP_STEPS.map((step, index) => (
                        <Step key={step} stepIndex={index} currentStep={activeStep}>
                            {step}
                        </Step>
                    ))}
                </Body>
            </Filler>
            <Footer>
                <StyledButton
                    className="success"
                    disabled={activeStep < 1}
                    onClick={() => setCurrentTab(activeStep - 1)}
                >
                    <LeftChevronIcon fill="white" height={19} width={19}/> Prev
                </StyledButton>
                <StyledButton
                    className="success"
                    disabled={isLoading || activeStep > SETUP_STEPS.length - 1}
                    onClick={handleNextButtonClick}
                >
                    Next <RightChevronIcon fill="white" height={19} width={19}/>
                </StyledButton>
            </Footer>
        </Container>
    );
}

export default Sidebar;
