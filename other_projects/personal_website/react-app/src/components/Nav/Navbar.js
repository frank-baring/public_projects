import React from 'react';
import styled from 'styled-components';
import Burger from "./Burger";


const Nav = styled.nav`
  width: 100%;
  height: 55px;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  
  .logo{
    padding: 15px 0;
  }
`

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

const Navbar = () => {
    return(
        <Nav>
            <div className="logo">
            </div>
            <Burger />
        </Nav>
    )
}

export default Navbar