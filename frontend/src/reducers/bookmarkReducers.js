import {
  COMICS_BOOKMARK_LIST_REQUEST,
  COMICS_BOOKMARK_LIST_SUCCESS,
  COMICS_BOOKMARK_LIST_FAIL,
  COMICS_BOOKMARK_ADD_FAIL,
  COMICS_BOOKMARK_ADD_SUCCESS,
  COMICS_BOOKMARK_ADD_REQUEST,
  COMICS_BOOKMARK_LIKE_REQUEST,
  COMICS_BOOKMARK_LIKE_SUCCESS,
  COMICS_BOOKMARK_LIKE_FAIL,
} from "../constants/bookmarkConstants";

export const comicBookmarkLikeReducer = (state = {}, action) => {
  switch (action.type) {
    case COMICS_BOOKMARK_LIKE_REQUEST:
      return { loading: true };

    case COMICS_BOOKMARK_LIKE_SUCCESS:
      return {
        ...state,
        loading: false,
        success: true,
        result: action.payload.result,
      };

    case COMICS_BOOKMARK_LIKE_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const comicBookmarkReducer = (state = {}, action) => {
  switch (action.type) {
    case COMICS_BOOKMARK_ADD_REQUEST:
      return { loading: true };

    case COMICS_BOOKMARK_ADD_SUCCESS:
      return { loading: false, success: true, msg: action.payload.status };

    case COMICS_BOOKMARK_ADD_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const comicBookmarkListReducer = (state = {}, action) => {
  switch (action.type) {
    case COMICS_BOOKMARK_LIST_REQUEST:
      return { loading: true };

    case COMICS_BOOKMARK_LIST_SUCCESS:
      return {
        ...state,
        loading: false,
        comics: action.payload.data,
        pages: action.payload.pages,
      };

    case COMICS_BOOKMARK_LIST_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};
