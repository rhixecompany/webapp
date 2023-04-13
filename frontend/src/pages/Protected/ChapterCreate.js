import React, { Fragment, useState } from "react";
import { useDispatch } from "react-redux";
import { createChapter } from "../../actions/chaptersActions";
import { Link } from "react-router-dom";
import { Form, Button } from "react-bootstrap";
const ChapterCreate = () => {
  const [name, setName] = useState("");

  const dispatch = useDispatch();

  const onSubmit = (e) => {
    e.preventDefault();

    dispatch(createChapter({ name }));
  };
  return (
    <Fragment>
      <Link to={"/admin/chapters"}>Go Back</Link>
      <Form onSubmit={onSubmit}>
        <Form.Group controlId="name">
          <Form.Label>Name</Form.Label>
          <Form.Control
            required
            type="name"
            placeholder="Enter name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Button type="submit" variant="primary">
          Create
        </Button>
      </Form>
    </Fragment>
  );
};

export default ChapterCreate;
