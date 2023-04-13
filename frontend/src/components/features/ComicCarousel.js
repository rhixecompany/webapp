import React, { useEffect } from "react";
import { listTopComics } from "../../actions/comicsActions";
import Loader from "./Loader";
import Message from "./Message";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { Carousel, Image } from "react-bootstrap";

const ComicCarousel = () => {
  const dispatch = useDispatch();
  const comicsTopRated = useSelector((state) => state.comicsTopRated);
  const { error, loading, comics } = comicsTopRated;
  useEffect(() => {
    dispatch(listTopComics());
  }, [dispatch]);
  return (
    <div>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Carousel pause="hover">
          {comics?.map((product) => (
            <Carousel.Item key={product._id}>
              <Link to={`/comic/${product._id}`}>
                <Image src={product.images} alt={product.title} fluid />
                <Carousel.Caption className="carousel.caption">
                  <h4>{product.title} </h4>
                </Carousel.Caption>
              </Link>
            </Carousel.Item>
          ))}
        </Carousel>
      )}
    </div>
  );
};

export default ComicCarousel;
