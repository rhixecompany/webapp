import React, { Fragment, useState } from "react";
import { Button, Form } from "react-bootstrap";
import { useHistory } from "react-router-dom";

const SearchBox = () => {
  const [keyword, setKeyword] = useState("");

  let history = useHistory();

  const submitHandler = (e) => {
    e.preventDefault();
    if (keyword) {
      history.push(`?keyword=${keyword}&page=1`);
    } else {
      history.push(history.push(history.location.pathname));
    }
    window.location.reload();
  };
  return (
    <Fragment>
      <Form onSubmit={submitHandler} inline>
        <Form.Control
          type="text"
          name="q"
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Search For Comics Everywhere..."
          className="mr-sm-2 ml-sm-5"
        ></Form.Control>
        <Button type="submit" variant="outline-success" className="p-1">
          Submit
        </Button>
      </Form>
    </Fragment>
  );
};

export default SearchBox;
