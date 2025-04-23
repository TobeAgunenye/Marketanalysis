import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';

const MyNavbar = () => (
  <Navbar bg="primary" variant="dark" expand="lg" fixed="top">
    <Container>
      <Navbar.Brand href="/home">Stock Dashboard</Navbar.Brand>
      <Navbar.Toggle aria-controls="navbarNav" />
      <Navbar.Collapse id="navbarNav">
        <Nav className="me-auto">
          {['Home', 'Overview', 'About', 'Pricing', 'Companies'].map((item) => (
            <Nav.Link key={item} href={`/${item.toLowerCase()}`}>
              {item}
            </Nav.Link>
          ))}
        </Nav>
        <Nav>
          <Nav.Link href="/login">Login</Nav.Link>
          <Nav.Link href="/register">Register</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
);

export default MyNavbar;
