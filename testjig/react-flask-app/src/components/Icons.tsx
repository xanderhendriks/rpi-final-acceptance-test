import React from 'react';

interface SVGProps {
  fill?: string;
  stroke?: string;
  viewBox?: string;

  [key: string]: any;
}

export const LeftChevronIcon = ({ fill = 'white', ...props }: SVGProps) => (
  <svg
    width="800px"
    height="800px"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <path
      d="M15 6L9.21261 11.7874V11.7874C9.09519 11.9048 9.09519 12.0952 9.21261 12.2126V12.2126L15 18"
      stroke={fill}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export const RightChevronIcon = ({ fill = 'white', ...props }: SVGProps) => (
  <svg
    width="800px"
    height="800px"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <path
      d="M9 18L14.7874 12.2126V12.2126C14.9048 12.0952 14.9048 11.9048 14.7874 11.7874V11.7874L9 6"
      stroke={fill}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export const CircleIcon = (props: SVGProps) => (
  <svg
    width="12px"
    height="12px"
    viewBox="0 0 1024 1024"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <circle cx="512" cy="512" r="256" fill={'white'} fillRule="evenodd" />
  </svg>
);

export const CheckmarkIcon = (props: SVGProps) => (
  <svg
    height="12px"
    width="12px"
    version="1.1"
    id="Capa_1"
    xmlns="http://www.w3.org/2000/svg"
    xmlnsXlink="http://www.w3.org/1999/xlink"
    viewBox="0 0 32 32"
    xmlSpace="preserve"
    {...props}
  >
    <g id="check_x5F_alt">
      <circle cx="16" cy="16" r="16" fill={'blue'} fillRule="evenodd" />
      <path
        style={{ fill: 'white' }}
        d="M16,0C7.164,0,0,7.164,0,16s7.164,16,16,16s16-7.164,16-16S24.836,0,16,0z M13.52,23.383
   L6.158,16.02l2.828-2.828l4.533,4.535l9.617-9.617l2.828,2.828L13.52,23.383z"
      />
    </g>
  </svg>
);
