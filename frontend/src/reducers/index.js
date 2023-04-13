import { combineReducers } from "redux";
import {
  userLoginReducer,
  userRegisterReducer,
  userDetailsReducer,
  userUpdateProfileReducer,
  userListReducer,
  userDeleteReducer,
  userUpdateReducer,
  userProfileReducer,
} from "./userReducers";
import {
  comicsListReducer,
  comicDetailsReducer,
  comicDeleteReducer,
  comicCreateReducer,
  comicUpdateReducer,
  comicsTopRatedReducer,
} from "./comicsReducers";
import {
  chaptersListReducer,
  chapterDetailsReducer,
  chapterDeleteReducer,
  chapterCreateReducer,
  chapterUpdateReducer,
  chaptersTopRatedReducer,
  chapterReviewCreateReducer,
} from "./chaptersReducers";
import { genreDetailsReducer, genresListReducer } from "./genresReducers";
import {
  categoryDetailsReducer,
  categorysListReducer,
} from "./categoryReducers";
import {
  comicBookmarkLikeReducer,
  comicBookmarkListReducer,
  comicBookmarkReducer,
} from "./bookmarkReducers";

const reducer = combineReducers({
  userLogin: userLoginReducer,
  comicsList: comicsListReducer,
  chaptersList: chaptersListReducer,
  userList: userListReducer,
  comicDetails: comicDetailsReducer,
  chapterDetails: chapterDetailsReducer,
  userDetails: userDetailsReducer,
  comicsBookmark: comicBookmarkReducer,
  comicBookmarkList: comicBookmarkListReducer,
  comicBookmarkLike: comicBookmarkLikeReducer,
  genresList: genresListReducer,
  genreDetails: genreDetailsReducer,
  categorysList: categorysListReducer,
  categoryDetails: categoryDetailsReducer,
  chapterDelete: chapterDeleteReducer,
  chapterCreate: chapterCreateReducer,
  chapterUpdate: chapterUpdateReducer,
  chaptersTopRatedReducer: chaptersTopRatedReducer,
  chapterReviewCreate: chapterReviewCreateReducer,
  comicDelete: comicDeleteReducer,
  comicCreate: comicCreateReducer,
  comicUpdate: comicUpdateReducer,
  comicsTopRated: comicsTopRatedReducer,
  userRegister: userRegisterReducer,
  userProfile: userProfileReducer,
  userUpdateProfile: userUpdateProfileReducer,
  userDelete: userDeleteReducer,
  userUpdate: userUpdateReducer,
});
export default reducer;
