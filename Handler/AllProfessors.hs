module Handler.AllProfessors where

import Import

$(deriveJSON defaultOptions ''Professor)

getAllProfessorsR :: Handler Html
getAllProfessorsR = do
  profs <- runDB $ selectList [] [] :: Handler [Entity Professor]
  returnJson profs

postAddProfessorR :: Handler Value
postAddProfessorR = do
  y <- runInputPost $ Professor
   <*> ireq textField "name"
   <*> ireq doubleField "rating"
  p_id <- runDB $ insert y
  return $ object [ "professor_key" .= p_id ]

