import React from "react";
import SearchBox from "./SearchBox";
import { useDispatch, useSelector } from "react-redux";
import { LinkContainer } from "react-router-bootstrap";
import { Navbar, Nav, Container, NavDropdown } from "react-bootstrap";
import {
  FaSignInAlt,
  FaSignOutAlt,
  FaUser,
  FaBookmark,
  FaTools,
  FaBook,
  FaBookOpen,
} from "react-icons/fa";
import { logout } from "../../actions/userActions";
const Navigation = () => {
  const dispatch = useDispatch();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const logoutHandler = () => {
    dispatch(logout());
  };
  return (
    <header>
      <Navbar
        className="navbar"
        bg="dark"
        variant="dark"
        expand="lg"
        collapseOnSelect
      >
        <Container>
          <LinkContainer to="/">
            <Navbar.Brand>Rhixescans</Navbar.Brand>
          </LinkContainer>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto ">
              <LinkContainer to="/blog">
                <Nav.Link>Series</Nav.Link>
              </LinkContainer>
              {userInfo ? (
                <NavDropdown title={userInfo.username} id="username">
                  <LinkContainer to="/profile">
                    <NavDropdown.Item>
                      {" "}
                      <FaTools /> Profile
                    </NavDropdown.Item>
                  </LinkContainer>
                  <LinkContainer to="/bookmarks">
                    <NavDropdown.Item>
                      {" "}
                      <FaBookmark /> Bookmarks
                    </NavDropdown.Item>
                  </LinkContainer>
                  <NavDropdown.Item onClick={logoutHandler}>
                    <FaSignOutAlt /> Logout
                  </NavDropdown.Item>
                </NavDropdown>
              ) : (
                <>
                  <LinkContainer to="/login">
                    <Nav.Link>
                      <FaSignInAlt /> Sign In
                    </Nav.Link>
                  </LinkContainer>
                  <LinkContainer to="/register">
                    <Nav.Link>
                      {" "}
                      <FaSignOutAlt />
                      Register
                    </Nav.Link>
                  </LinkContainer>
                </>
              )}
              {userInfo && userInfo.isAdmin && (
                <NavDropdown title="Admin" id="adminmenu">
                  <LinkContainer to="/admin/users">
                    <NavDropdown.Item>
                      {" "}
                      <FaUser /> Users
                    </NavDropdown.Item>
                  </LinkContainer>
                  <LinkContainer to="/admin/comicslist">
                    <NavDropdown.Item>
                      {" "}
                      <FaBook />
                      Comics
                    </NavDropdown.Item>
                  </LinkContainer>
                  <LinkContainer to="/admin/chapterslist">
                    <NavDropdown.Item>
                      {" "}
                      <FaBookOpen />
                      Chapters
                    </NavDropdown.Item>
                  </LinkContainer>
                  <LinkContainer to="/admin/scraper">
                    <NavDropdown.Item>Scraper</NavDropdown.Item>
                  </LinkContainer>
                </NavDropdown>
              )}
            </Nav>
            <SearchBox />
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
};

export default Navigation;
