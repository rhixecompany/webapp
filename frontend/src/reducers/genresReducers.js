import {
  GENRES_LIST_REQUEST,
  GENRES_LIST_SUCCESS,
  GENRES_LIST_FAIL,
  GENRES_DETAILS_REQUEST,
  GENRES_DETAILS_SUCCESS,
  GENRES_DETAILS_FAIL,
} from "../constants/genresConstants";

export const genresListReducer = (state = {}, action) => {
  switch (action.type) {
    case GENRES_LIST_REQUEST:
      return { loading: true };

    case GENRES_LIST_SUCCESS:
      return { ...state, loading: false, genres: action.payload.result };

    case GENRES_LIST_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const genreDetailsReducer = (state = {}, action) => {
  switch (action.type) {
    case GENRES_DETAILS_REQUEST:
      return { loading: true };

    case GENRES_DETAILS_SUCCESS:
      return {
        ...state,
        loading: false,
        genre: action.payload.result,
        comics: action.payload.comics,
      };

    case GENRES_DETAILS_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};
