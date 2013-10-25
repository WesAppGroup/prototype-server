{-# OPTIONS_GHC -fno-warn-orphans #-}
module Handler.Event where

import Import

$(deriveJSON defaultOptions ''Event)

getEventR :: EventId -> Handler Value
getEventR eId = runDB (get404 eId) >>= returnJson

addEventR :: Handler Value
addEventR = do
   ev <- runInputGet $ Event
           <$> ireq textField "name"
	   <*> ireq intField "locationId"
	   <*> ireq intField "time"
	   <*> ireq textField "link"
	   <*> ireq textField "description"
	   <*> ireq intField "category"
	   <*> ireq doubleField "latitude"
	   <*> ireq doubleField "longitude"
   eId <- runDB $  insert ev
   returnJson [ "event_id" .= eId ]
