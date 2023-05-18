
local retval, start_mute = reaper.GetUserInputs("Start from", 1, " (0 or 1 means : here or next  )", "")
if retval == false then
    return
end

start_mute = tonumber(start_mute)

if start_mute ~= 0 and start_mute ~= 1 then
    reaper.ShowMessageBox("Pleae input 0 or 1", "error!", 0)
    return
end


local track = reaper.GetSelectedTrack(0, 0)
if track == nil then
    reaper.ShowMessageBox("Select Track!", "error!", 0)
    return
end


local item_count = reaper.CountTrackMediaItems(track)


for i = 0, item_count - 1 do
    local item = reaper.GetTrackMediaItem(track, i)
    if item then
        if (i + start_mute) % 2 == 0 then
            reaper.SetMediaItemInfo_Value(item, "B_MUTE", 1)
        else
            reaper.SetMediaItemInfo_Value(item, "B_MUTE", 0)
        end
    end
end


reaper.UpdateArrange()

