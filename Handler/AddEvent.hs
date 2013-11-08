{-# OPTIONS_GHC -fno-warn-orphans #-}
module Handler.AddEvent where

import Import
import Data.Maybe(fromJust)

$(deriveJSON defaultOptions ''Event)

getAddEventR :: Handler Value
getAddEventR = do
   ev <- runInputGet $ Event
           <$> ireq textField "name"
       <*> ireq textField "location"
       <*> ireq intField "time"
       <*> ireq textField "link"
       <*> ireq textField "description"
       <*> ireq textField "category"
       <*> ireq doubleField "latitude"
       <*> ireq doubleField "longitude"
   eId <- runDB $  insert ev
   returnJson [ "event_id" .= eId ]
