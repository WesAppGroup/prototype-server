{-# OPTIONS_GHC -fno-warn-orphans #-}
module Handler.AddEvent where

import Import
import Data.Maybe(fromJust)
import Data.Time

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
   events <- runDB $ selectList [ EventName ==. (eventName ev) ] []
   if null events
    then do
      eId <- runDB $  insert ev
      returnJson [ "event_id" .= eId ]
    else do
      returnJson [ "error" .= ("duplicate event" :: Text) ]

getClearOldEventsR :: Handler Value
getClearOldEventsR = do
   (UTCTime (ModifiedJulianDay day) _) <- liftIO $ getCurrentTime
   let utcTime = fromInteger $ (day * 86400) - 3538252800 :: Int
   let oldest = utcTime - (86400 * 7)
   runDB $ deleteWhere [ EventTime <. oldest ]
   returnJson [ "status" .= ( "ok" :: Text ) ]
