{-# OPTIONS_GHC -fno-warn-orphans #-}
module Handler.Section where

import Import

$(deriveJSON defaultOptions ''Section)

getSectionR :: SectionId -> Handler Value
getSectionR sId = do
    section <- runDB $ get404 sId
    returnJson section

getAllSectionR :: Handler Value
getAllSectionR = do
    sections <- (runDB $ selectList [] []) :: Handler [Entity Section]
    returnJson sections

getSectionsForCourseR :: Int -> Int -> Handler Value
getSectionsForCourseR courseId semester = do
    sections <- runDB $ selectList [ SectionCourseid ==. courseId, SectionSemester ==. semester ] []
    returnJson sections

postAddSectionR :: Handler Value
postAddSectionR = do
  s <- runInputPost $ Section
   <$> ireq intField "course_uid"
   <*> ireq intField "semester"
   <*> ireq textField "time"
   <*> ireq textField "professors"
   <*> ireq textField "location"
   <*> ireq textField "seats_available"
  s_id <- runDB $ insert s
  return $ object [ "section_key" .= s_id ]

