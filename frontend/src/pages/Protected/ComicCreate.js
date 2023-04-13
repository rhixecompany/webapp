import React, { Fragment, useState } from "react";
import { useDispatch } from "react-redux";
import { createComic } from "../../actions/comicsActions";
import { Link } from "react-router-dom";
import { Form, Button } from "react-bootstrap";
const ComicCreate = () => {
  const [title, setTitle] = useState("");

  const dispatch = useDispatch();

  const onSubmit = (e) => {
    e.preventDefault();

    dispatch(createComic({ title }));
  };
  return (
    <Fragment>
      <Link to={"/admin/comics"}>Go Back</Link>
      <Form onSubmit={onSubmit}>
        <Form.Group controlId="title">
          <Form.Label>Title</Form.Label>
          <Form.Control
            required
            type="title"
            placeholder="Enter title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Button type="submit" variant="primary">
          Create
        </Button>
      </Form>
    </Fragment>
  );
};

export default ComicCreate;
