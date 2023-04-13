import React, { useState, useEffect } from "react";
import { Form, Button, Row, Col, Table, Image } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import FormContainer from "../../components/features/FormContainer";
import { getUserProfile, updateUserProfile } from "../../actions/userActions";
import { USER_UPDATE_PROFILE_RESET } from "../../constants/userConstants";
import { FaEdit, FaTrash } from "react-icons/fa";
import { Link } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import { deleteComic } from "../../actions/comicsActions";
const Profile = () => {
  const [username, setUsername] = useState("");
  const [first_name, setFirst_name] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");

  const dispatch = useDispatch();
  const userProfile = useSelector((state) => state.userProfile);
  const { error, loading, user, comics } = userProfile;
  const userUpdateProfile = useSelector((state) => state.userUpdateProfile);
  const { success } = userUpdateProfile;
  const comicDelete = useSelector((state) => state.comicDelete);
  const { success: successDelete } = comicDelete;
  useEffect(() => {
    if (success) {
      dispatch({ type: USER_UPDATE_PROFILE_RESET });
      window.location.reload();
    }
    if (!user.username) {
      dispatch(getUserProfile());
    } else {
      setFirst_name(user.first_name);
      setUsername(user.username);
      setEmail(user.email);
    }
  }, [dispatch, user, success, successDelete]);
  const submitHandler = (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
    } else {
      dispatch(
        updateUserProfile({
          id: user.id,
          first_name: first_name,
          username: username,
          email: email,
          password: password,
        })
      );

      setMessage("");
    }
  };
  const deleteHandler = (id) => {
    if (window.confirm(`Are you sure you want to delete:${id}`)) {
      dispatch(deleteComic(id));
    }
  };
  return (
    <>
      <Row>
        <Col md={3}>
          <FormContainer>
            <h2>User Profile</h2>
            {message && <Message variant="danger">{message}</Message>}
            {error && <Message variant="danger">{error}</Message>}
            {loading && <Loader />}
            <Form onSubmit={submitHandler}>
              <Form.Group controlId="username">
                <Form.Label>Username</Form.Label>
                <Form.Control
                  required
                  type="username"
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                ></Form.Control>
              </Form.Group>

              <Form.Group controlId="email">
                <Form.Label>Email Address</Form.Label>
                <Form.Control
                  required
                  type="email"
                  placeholder="Enter Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                ></Form.Control>
              </Form.Group>

              <Form.Group controlId="firstname">
                <Form.Label>First Name</Form.Label>
                <Form.Control
                  required
                  type="firstname"
                  placeholder="Enter firstname"
                  value={first_name}
                  onChange={(e) => setFirst_name(e.target.value)}
                ></Form.Control>
              </Form.Group>

              <Form.Group controlId="password">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Enter Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                ></Form.Control>
              </Form.Group>

              <Form.Group controlId="passwordConfirm">
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Confirm Password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                ></Form.Control>
              </Form.Group>

              <Button type="submit" variant="primary">
                Update
              </Button>
            </Form>
          </FormContainer>
        </Col>
        <Col md={9}>
          <h2>Comics List</h2>
          <Table
            className="table table-sm text-white"
            striped
            bordered
            hover
            responsive
          >
            <thead>
              <tr>
                <th>Title</th>
                <th>Image</th>
                <th></th>
                <th></th>
              </tr>
            </thead>

            <tbody>
              {comics?.map((comic) => (
                <tr key={comic._id}>
                  <td>
                    <Link
                      className="text-white btn btn-sm"
                      to={`/comic/${comic._id}/`}
                    >
                      {comic.title}
                    </Link>
                  </td>
                  <td>
                    <div>
                      <Link
                        className="text-white btn btn-sm"
                        to={`/comic/${comic._id}/`}
                      >
                        <Image
                          className="img-fluid"
                          src={comic.images}
                          alt={comic.title}
                        />
                      </Link>
                    </div>
                  </td>

                  <td>
                    <LinkContainer
                      className="text-white btn btn-sm"
                      to={`/admin/comic/${comic._id}/edit`}
                    >
                      <Button variant="white" className="btn-sm">
                        Edit <FaEdit className="fas fa-edit" />
                      </Button>
                    </LinkContainer>
                  </td>
                  <td>
                    <Button
                      variant="danger"
                      className="btn-sm"
                      onClick={() => deleteHandler(comic._id)}
                    >
                      Delete <FaTrash className="fas fa-trash" />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Col>
      </Row>
    </>
  );
};

export default Profile;
