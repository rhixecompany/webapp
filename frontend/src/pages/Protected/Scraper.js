import React, { useState } from "react";
import { Container, Row, Col, Form, Button } from "react-bootstrap";

const Scraper = () => {
  const [url, setUrl] = useState("");

  const onSubmit = (e) => {
    e.preventDefault();

    console.log(url);
  };
  return (
    <Container>
      <Row>
        <h1>Download Comics</h1>
        <Col>
          <Form onSubmit={onSubmit}>
            <Form.Group controlId="url">
              <Form.Label>Url</Form.Label>
              <Form.Control
                required
                type="url"
                placeholder="Enter url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              ></Form.Control>
            </Form.Group>

            <Button type="submit" variant="primary">
              Create
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default Scraper;
