{-# OPTIONS_GHC -fno-warn-orphans #-}
module Handler.AddEvent where

import Import
import Data.Maybe(fromJust)

$(deriveJSON defaultOptions ''Event)

postAddEventR :: Handler Value
postAddEventR = do
   ev <- runInputGet $ Event
           <$> ireq textField "name"
       <*> ((fromJust . fromPathPiece) <$> ireq textField "locationId")
       <*> ireq intField "time"
       <*> ireq textField "link"
       <*> ireq textField "description"
       <*> ireq intField "category"
       <*> ireq doubleField "latitude"
       <*> ireq doubleField "longitude"
   eId <- runDB $  insert ev
   returnJson [ "event_id" .= eId ]
