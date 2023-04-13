import React, { Fragment, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { listComicDetails } from "../../actions/comicsActions";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import Rating from "../../components/features/Rating";
import { ListGroup, Container, Image } from "react-bootstrap";
import { Link } from "react-router-dom";
const Comic = () => {
  const { slug } = useParams();
  const dispatch = useDispatch();
  const { comic, error, loading, chapters } = useSelector(
    (state) => state.comicDetails
  );
  useEffect(() => {
    dispatch(listComicDetails(slug));
  }, [dispatch, slug]);
  return (
    <Fragment>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container>
          <div>
            <Image
              fluid
              className="img-fluid"
              src={comic?.image}
              alt={comic?.image}
            />
          </div>
          <div>
            <h1>{comic?.title}</h1>
            <Rating
              value={comic.rating}
              text={`${comic.rating} Rating`}
              color={"#f8e825"}
            />
          </div>
          <div>
            {chapters?.length > 0 ? (
              <ListGroup variant="flush">
                {chapters?.map((chapter) => {
                  return (
                    <ListGroup.Item key={chapter.id}>
                      <strong>Name:</strong>
                      <Link to={`/chapter/${chapter.name}/`}>
                        {chapter.name}
                      </Link>
                    </ListGroup.Item>
                  );
                })}
              </ListGroup>
            ) : (
              <Message variant="danger">{<small>No Chapter</small>}</Message>
            )}
          </div>
        </Container>
      )}
    </Fragment>
  );
};

export default Comic;
