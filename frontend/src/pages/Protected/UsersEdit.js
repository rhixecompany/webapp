import React, { useEffect, Fragment, useState } from "react";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import FormContainer from "../../components/features/FormContainer";
import { useDispatch, useSelector } from "react-redux";
import { getUserDetails, updateUser } from "../../actions/userActions";
import { Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { USER_UPDATE_RESET } from "../../constants/userConstants";
import { useParams } from "react-router-dom";
const UsersEdit = () => {
  const { id } = useParams();
  const [username, setUsername] = useState("");
  const [first_name, setFirst_name] = useState("");
  const [email, setEmail] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const dispatch = useDispatch();

  const userDetails = useSelector((state) => state.userDetails);
  const { loading, error, user } = userDetails;
  const userUpdate = useSelector((state) => state.userUpdate);
  const {
    error: errorUpdate,
    loading: loadingUpdate,
    success: successUpdate,
  } = userUpdate;
  useEffect(() => {
    if (successUpdate) {
      dispatch({ type: USER_UPDATE_RESET });
      //window.location.reload();
    }
    if (!user.username || user._id !== Number(id)) {
      dispatch(getUserDetails(id));
    } else {
      setFirst_name(user.first_name);
      setUsername(user.username);
      setEmail(user.email);
      setIsAdmin(user.isAdmin);
    }
  }, [
    dispatch,
    id,
    user.username,
    user.id,
    user.email,
    user.isAdmin,
    successUpdate,
    user._id,
    user.first_name,
  ]);

  const submitHandler = (e) => {
    e.preventDefault();

    dispatch(updateUser(id, username, first_name, email, isAdmin));
  };

  return (
    <Fragment>
      <Link to="/admin/users" className="btn btn-light my-3">
        Go Back
      </Link>
      <FormContainer>
        <h2>Edit User</h2>
        {loadingUpdate && <Loader />}
        {errorUpdate && <Message variant="danger">{errorUpdate}</Message>}
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <Form onSubmit={submitHandler}>
            <Form.Group controlId="username">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="username"
                placeholder="Enter Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              ></Form.Control>
            </Form.Group>

            <Form.Group controlId="email">
              <Form.Label>Email Address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
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

            <Form.Group controlId="isadmin">
              <Form.Check
                type="checkbox"
                label="Is Admin"
                checked={isAdmin}
                onChange={(e) => setIsAdmin(e.target.checked)}
              ></Form.Check>
            </Form.Group>

            <Button type="submit" variant="primary">
              Update
            </Button>
          </Form>
        )}
      </FormContainer>
    </Fragment>
  );
};

export default UsersEdit;
