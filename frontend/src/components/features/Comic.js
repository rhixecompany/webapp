import React from "react";
import { Link } from "react-router-dom";
import { ListGroup, Button, Card } from "react-bootstrap";
import Rating from "./Rating";
import Message from "./Message";
const Comic = ({ comic }) => {
  return (
    <Card className="my-3 p-1 rounded box">
      <div>
        <Link to={`/comic/${comic._id}`}>
          <Card.Img src={comic.images} variant="top" />
        </Link>
        <div>
          <Button variant="default" className="btn btn-sm">
            <Link to={`/category/${comic.category?._id}/`}>
              {comic.category?.name}
            </Link>
          </Button>
        </div>
      </div>

      <Card.Body className="Boxcontent">
        <Card.Title as="div">
          <h5>
            <Link to={`/comic/${comic._id}`}>{comic.title.substr(0, 70)}</Link>
          </h5>
        </Card.Title>

        <Card.Text as="div">
          <Rating
            value={comic.rating}
            text={`Rating:${comic.rating}`}
            color={"#f8e825"}
          />
        </Card.Text>

        <Card.Text as="div">
          {comic.chapters?.length > 0 ? (
            <ListGroup variant="flush">
              <strong>Chapters:</strong>
              {comic.chapters?.map((chapter) => {
                return (
                  <ListGroup.Item key={chapter._id}>
                    <Link to={`/chapter/${chapter._id}/`}>{chapter.name}</Link>
                  </ListGroup.Item>
                );
              })}
            </ListGroup>
          ) : (
            <Message variant="info">{<small>No Chapter</small>}</Message>
          )}
        </Card.Text>
      </Card.Body>
    </Card>
  );
};

export default Comic;
