{-# OPTIONS_GHC -fno-warn-orphans #-}
module Handler.Section where

import Import

$(deriveJSON defaultOptions ''Section)

getSectionR :: SectionId -> Handler Value
getSectionR sId = do
    section <- runDB $ get404 sId
    returnJson section

postAddSectionR :: Handler Value
postAddSectionR = do
  s <- runInputPost $ Section
   <*> ireq textField "name"
   <*> ireq intField "course_uid"
   <*> ireq textField "permissionsRequired"
   <*> ireq textField "fr"
   <*> ireq textField "so"
   <*> ireq textField "jr_NonMajor"
   <*> ireq textField "jr_Major"
   <*> ireq textField "sr_NonMajor"
   <*> ireq textField "sr_Major"
   <*> ireq textField "grad_Major"
   <*> ireq textField "additional_Requirements"
   <*> ireq textField "time"
   <*> ireq textField "professors"
   <*> ireq textField "location"
   <*> ireq textField "major_readings"
   <*> ireq intField "seats_available"
   <*> ireq textField "assignments_and_examinations"
  s_id <- runDB $ insert s
  return $ object [ "section_key" .= s_id ]

