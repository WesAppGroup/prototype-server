module Handler.Course where

import Import
import Data.List (isInfixOf)
import Data.Char (toLower)
import Data.Text (unpack)

$(deriveJSON defaultOptions ''Course)


getCourseR :: Handler Value
getCourseR = do
  courses <- runDB $ selectList [] [] :: Handler [Entity Course]
  returnJson courses

getSearchCourseR :: String -> Handler Value
getSearchCourseR query = do
  courses <- runDB $ selectList [] [] :: Handler [Entity Course]
  returnJson $ filter (isLike query) courses
 
isLike :: String -> (Entity Course) -> Bool
isLike query ent = (words . (map toLower) $ query) `isIn` ((map toLower) . (\x -> (unpack . courseTitle $ x) ++ (unpack . courseNumber $ x) ++  (unpack . courseDepartment $ x)) . entityVal $ ent)

isIn :: [String] -> String -> Bool
isIn [] _ = True
isIn (x:xs) q = (x `isInfixOf` q) && (isIn xs q)

getClearR :: String -> Handler Value
getClearR pwd = do
  if pwd == "thisiswhy"
    then
      runDB $ deleteWhere ([] :: [Filter Course])
      runDB $ deleteWhere ([] :: [Filter Section])
      return $ object [ "result" .= ("ok" :: Text) ]
    else
      return $ object [ "result" .= ("error" :: Text) ]

postAddCourseR :: Handler Value
postAddCourseR = do
  x <- runInputPost $ Course
    <$> ireq textField "genEdArea"
    <*> ireq textField "title"
    <*> ireq textField "number"
    <*> ireq intField "courseid"
    <*> ireq textField "semester"
    <*> ireq textField "department"
    <*> ireq textField "description"
  cId <- runDB $ insert x
  return $ object [ "course_key" .= cId ]

      
