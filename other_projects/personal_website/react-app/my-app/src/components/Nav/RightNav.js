import React from 'react';
import styled from 'styled-components';

const Ul = styled.ul`
    list-style: none;
    display: flex;
    flex-flow: row nowrap;
  
    li{
      padding: 25px 10px;
    }
  
      flex-flow: column nowrap;
      background-color: #0D2538;
      position: fixed;
      transform: ${({ open }) => open ? 'translateX(0)' : 'translateX(100%)'};
      top: 0;
      right: 0;
      height: 100vh;
      width: 300px;
      padding-top: 3.5rem;
      transition: transform 0.3s ease-in-out;
      
      li {
        color: #fff;
      }
    }
`;

const RightNav = ({ open }) => {
    return (
        <Ul open={open}>
            <li className="font-link">Resumé</li>
            <li className="font-link">Contact</li>
        </Ul>
    )
}

export default RightNav