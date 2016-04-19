%analyze json file from craiglist
roomdata = loadjson('atl100.json');

for ii = 1:length(roomdata)
    temp = cell2mat(roomdata{ii}.price);
    if ~isempty(temp)
        pricelist(ii) = str2num(temp(2:end));
    else
        pricelist(ii) = NaN;
    end
    bikinglist(ii) = roomdata{ii}.bikingtime;
    drivinglist(ii) = roomdata{ii}.drivingtime;
    transitlist(ii) = roomdata{ii}.transittime;
end

figure(1)
plot(pricelist,bikinglist/60,'o')
title('Biking time to Emory University vs Rent')
xlabel('Rent ($/month)')
ylabel('Biking time in morning traffic (min)')

figure(2)
plot(transitlist/60,drivinglist/60,'o')
title('Public transit vs Driving')
xlabel('Public transit time in morning traffic (min)')
ylabel('Driving time in morning traffic (min)')